#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define MAXNAME 80  /* maximum permitted name size, not including \0 */
#define NPITS 6  /* number of pits on a side, not including the end pit */
#define NPEBBLES 4 /* initial number of pebbles per pit */
#define MAXMESSAGE (MAXNAME + 50) 
#define WELCOME_MESSAGE "Welcome to Mancala. What is your name?\r\n" /*Message for new comers */
#define ANNOUNCE_JOIN " has joined the game!\r\n" /*Announce message sent to all existing players when new player joins */

int port = 53410;
int listenfd;

struct player {
    int fd;
    char name[MAXNAME+1]; 
    int pits[NPITS+1];  // pits[0..NPITS-1] are the regular pits 
                        // pits[NPITS] is the end pit
    //other stuff undoubtedly needed here
    int turn; // This is an indicator, 0 means not this player's turn, 1 means this player's turn, -1 means he is a fake player
    struct player *previous;
    struct player *next;
};

struct player *playerlist = NULL;

extern void parseargs(int argc, char **argv);
extern void makelistener();
extern int compute_average_pebbles();
extern int game_is_over();  /* boolean */
extern void broadcast(char *s);  /* you need to write this one */
extern int accept_connection(int fd);  // Accept the connection from client, add him into the playerlist
extern int find_network_newline(const char *buf, int n);
extern int player_move(struct player *p_move, int pit);
extern void display_game_board();
extern struct player *hand_over_turn(struct player *current_player);


int main(int argc, char **argv) {
    char msg[MAXMESSAGE];

    parseargs(argc, argv);
    makelistener();
    
    //We prepare to listen to multiple
    // file descriptors by initializing a set of file descriptors
    int max_fd = listenfd;
    fd_set all_fds;
    FD_ZERO(&all_fds);
    FD_SET(listenfd, &all_fds);

    while (!game_is_over()) {
        fd_set listen_fds = all_fds;
        int nready = select(max_fd+1, &listen_fds, NULL, NULL, NULL);
        if (nready == -1) {
            perror("server: select");
            exit(1);
        }

        // Is it the original socket? Create a new connection ..
        // This chunk of code handles the case that when a new client is connected to the server,
        // At this point, this player hasn't given a name, so he is added into the playerlist
	    if (FD_ISSET(listenfd, &listen_fds)) {
	        int client_fd = accept_connection(listenfd);
            if (client_fd > max_fd) { // A new player is in now
                max_fd = client_fd;
            }
            FD_CLR(client_fd, &listen_fds);
            FD_SET(client_fd, &all_fds);
            struct player *fake_player = malloc(sizeof(struct player));
            fake_player->fd = client_fd;
            int pebble = compute_average_pebbles();
            for (int pit = 0; pit < 6; pit++) {
                (fake_player->pits)[pit] = pebble;
            }
            (fake_player->pits)[6] = 0;
            fake_player->turn = -1;
            fake_player->previous = NULL;    

            if (playerlist == NULL) { // The first fake player
                fake_player->next = NULL;
                playerlist = fake_player;          
            } else { // Adding this fake player to the linked list
                playerlist->previous = fake_player;
                fake_player->next = playerlist;
                playerlist = fake_player;
            }            
        }
        
        struct player *next_player = NULL;
        
        // This chunk of code handle the players in the playerlist
        for (struct player *p = playerlist; p  && p != (struct player *)0x90; p=p->next) {
            if (FD_ISSET(p->fd, &listen_fds)) {  // To those players who give a message to the server

                /* This chunk of code is to handle the player who has the turn and give their response,
                 * this player could make a move or disconnects from the server
                 */
                if (p->turn == 1) { // This player's turn
                    char move[MAXMESSAGE] = {'\0'};
                    int num_read = read(p->fd, move, MAXMESSAGE);

                    if (num_read == 0) {     // This player disconnects

                        FD_CLR(p->fd, &all_fds);
                        FD_CLR(p->fd, &listen_fds);

                        next_player = hand_over_turn(p); // this next_player will have the turn
                        if (next_player->fd == p->fd) {
                            next_player = NULL;
                        }

                        if (p->previous == NULL && p->next == NULL) { // This is the case that this player is the only player in playerlist
                            playerlist = NULL;
                        } else if (p->previous == NULL) { // This is the case that this player is the head of the linked list
                            (p->next)->previous = NULL;
                            playerlist = p->next;
                        } else if (p->next == NULL) { // This is the case that this player is the tail of the linked list
                            (p->previous)->next = NULL;
                        } else { // This is the case that his player is in the middle of the linked list
                            (p->previous)->next = p->next;   // connect the players in playerlist
                            (p->next)->previous = p->previous;
                        }

                        char player_left_game[MAXMESSAGE];
                        sprintf(player_left_game, "%s has left the game\r\n", p->name);
                        broadcast(player_left_game);
                        printf("%s has left the game\n", p->name);
                        display_game_board();
                        p->next = NULL;
                        p->previous = NULL;
                        free(p);

                    } else {     // Case that this player response a message
                        FD_CLR(p->fd, &listen_fds);
                        int move_pit = strtol(move, NULL, 10);
                        if (move_pit > 5) { // The user tried an invalid move
                            write(p->fd, "Invalid move\r\n", strlen("Invalid move\r\n"));
                        } else if ((p->pits[move_pit]) == 0) { // The user tried to move on an empty pit
                            write(p->fd, "Please move on a non-empty pit\r\n", strlen("Please move on a non-empty pit\r\n"));
                        } else {
                            char player_made_move[MAXMESSAGE];
                            sprintf(player_made_move, "%s has made move on pit %d\r\n", p->name, move_pit);
                            broadcast(player_made_move);
                            printf("%s has made move on pit %d\n", p->name, move_pit);

                            int extra_move;
                            extra_move = player_move(p, move_pit); // player makes his move
                            display_game_board();
                            
                            if (extra_move == 0) { // He doesn't get an extra move
                                p->turn = 0;
                                next_player = hand_over_turn(p);
                                if (next_player->fd == p->fd) {
                                    next_player = NULL;
                                    p->turn = 1;
                                }
                            } else {
                                write(p->fd, "Your Move?\r\n", strlen("Your Move?\r\n"));
                            }
                            // Otherwise p->turn is still 1

                        }
                    }
                } 

                /* This chunk of code is to handle the response of those players who give response when it's
                 * not their turn. They could give garbage information, or disconnects from the server
                 */
                
                else if (p->turn == 0) { 
                    // Two cases, either this player disconnect from the server or this player tries to move
                    char garbage_message[MAXMESSAGE];
                    int num_read = read(p->fd, garbage_message, MAXMESSAGE);
                    
                    if (num_read == 0) { // This player disconnects
                        FD_CLR(p->fd, &all_fds);
                        FD_CLR(p->fd, &listen_fds);


                        if (next_player && next_player->fd == p->fd) { // Disconnected but he was suppose to be the next_player
                            next_player = hand_over_turn(p);
                            if (next_player->fd == p->fd) {
                                next_player = NULL;
                            }
                        }               
                    

                        if (p->previous == NULL && p->next == NULL) { // This is the case that this player is the only player in playerlist
                            playerlist = NULL;
                        } else if (p->previous == NULL) { // This is the case that this player is the head of the linked list
                            (p->next)->previous = NULL;
                            playerlist = p->next;
                        } else if (p->next == NULL) { // This is the case that this player is the tail of the linked list
                            (p->previous)->next = NULL;
                        } else { // This is the case that his player is in the middle of the linked list
                            (p->previous)->next = p->next;  
                            (p->next)->previous = p->previous;
                        } 
                        char player_left_game[MAXMESSAGE];
                        sprintf(player_left_game, "%s has left the game\r\n", p->name);
                        broadcast(player_left_game);
                        printf("%s has left the game\n", p->name);
                        display_game_board();
                        p->next = NULL;
                        p->previous = NULL;
                        free(p);
                    } else { // if the player has given garbage message when it's not his turn.
                        write(p->fd, "It is not your move.\r\n", sizeof("It is not your move.\r\n"));
                        FD_CLR(p->fd, &listen_fds);
                    }
                } 


                /* This chunk of code is to handle the response of those fake_players who haven't given their name yet,
                 * They could possibly give a name or disconnects from the server
                 */
                else {
                    
                    FD_CLR(p->fd, &listen_fds);
                    
                    char name[MAXNAME + 3] = {'\0'};
                    int inbuf = 0;                 // How many bytes currently in the buffer?
                    int room = sizeof(name) - 1;    // How many bytes remaining in the buffer?
                    char *after = name;            // Pointer to position after the data in buf  
                    
                    int nbytes;                   // number of bytes read in this time
                    int name_read = 0;       // name_read = 1 if we have read in a user name
                    
                    // read in the user name into the buffer
                    while (name_read == 0 && (nbytes = read(p->fd, after, room)) > 0) {
                        inbuf += nbytes;
                        int where;
                        if ((where = find_network_newline(name, inbuf)) >= 0) {
                            name[where] = '\0';    // clear out the special character \r and \n
                            name[where+1] = '\0';
                            name_read = 1;
                        }
                        after = name + inbuf;
                        room = MAXNAME + 2 - inbuf;
                    }
                  
                
                    if (nbytes == 0 && strlen(name) == 0 && name_read == 0) { // Fake player disconnects from the server
                        FD_CLR(p->fd, &all_fds);
                        if (p->previous == NULL && p->next == NULL) { // This is the case that this player is the only player in playerlist
                            playerlist = NULL;
                        } else if (p->previous == NULL) { // This is the case that this player is the head of the linked list
                            (p->next)->previous = NULL;
                            playerlist = p->next;
                        } else if (p->next == NULL) { // This is the case that this player is the tail of the linked list
                            (p->previous)->next = NULL;
                        } else { // This is the case that his player is in the middle of the linked list
                            (p->previous)->next = p->next;  
                            (p->next)->previous = p->previous;
                        } 
                        p->next = NULL;
                        p->previous = NULL;                        
                        free(p);                   
                    } else if (name_read == 0 || strlen(name) > MAXNAME) { // name too long case
                        write(p->fd, "The maximum permitted size of name is 80\r\n", strlen("The maximum permitted size of name is 80\r\n"));
                    } else if (strlen(name) == 0 && name_read == 1) { // empty string name case, not accepted
                        write(p->fd, "Please don't give an empty name\r\n", strlen("Please don't give an empty name\r\n"));
                    } else {  // We have read in an actual name
                        
                        int used_name = 0; // this is a indicator for used name, 0 implies not used, 1 implies used (unacceptable name)
                        struct player *player = playerlist;
                        while (player && used_name == 0){
                            if (player->turn != -1 && strcmp(name, player->name) == 0) { //used name found, can't use this name
                                used_name = 1;
                            }
                            player = player->next;
                        }
                        if (used_name == 1) {
                            write(p->fd, "This name is already used\r\n", strlen("This name is already used\r\n"));
                        } else if (used_name == 0) {
                            // Give this player a name, and decide he's turn
                            strcpy(p->name, name);                          

                            if (p->previous == NULL && p->next == NULL) { // He is the only player 
                                p->turn = 1;
                            } else { // He is not the only player
                                int flag = 0; // This flag indicates that if we have found an actual player inside playerlist before he joins
                                              // 0 indicates we haven't found, 1 indicates we have found
                                p->turn = 0;
                                for (struct player *u = playerlist; flag == 0 && u; u = u->next) {
                                    if (u->turn != -1) {
                                        flag = 1; // found one
                                    }
                                }
                                if (flag == 0) {
                                    p->turn = 1;
                                }
                            }                         
                            // Announce that we got a new player into the game
                            
                            char announce[MAXMESSAGE];
                            sprintf(announce, "%s has joined the game!\r\n", p->name);
                            broadcast(announce);
                            printf("%s has joined the game!\n", p->name);
                            display_game_board();
                        }
                    }
                }
            }
        }

        if (next_player) {
            next_player->turn = 1;
        }

        /* This chunk of code make annoucement to everyone about who's move it is,
         * Also tells everyone the current game status
         */
        if (next_player && !game_is_over()) {
            next_player->turn = 1;
            write(next_player->fd, "Your Move?\r\n", strlen("Your Move?\r\n"));
            char whos_move[MAXMESSAGE];
            for (struct player *p = playerlist; p; p=p->next) {
                if (p->turn == 1) {
                    sprintf(whos_move, "It is %s's move\r\n", p->name);
                } 
            }
            for (struct player *p = playerlist; p; p=p->next) {
                if (p->turn == 0) {
                    write(p->fd, whos_move, strlen(whos_move));
                }
            }
        }
    }

    broadcast("Game over!\r\n");
    printf("Game over!\n");
    for (struct player *p = playerlist; p; p = p->next) {
        int points = 0;
        for (int i = 0; i <= NPITS; i++) {
            points += p->pits[i];
        }
        printf("%s has %d points\r\n", p->name, points);
        snprintf(msg, MAXMESSAGE, "%s has %d points\r\n", p->name, points);
        broadcast(msg);
    }

    return 0;
}


void parseargs(int argc, char **argv) {
    int c, status = 0;
    while ((c = getopt(argc, argv, "p:")) != EOF) {
        switch (c) {
        case 'p':
            port = strtol(optarg, NULL, 0);  
            break;
        default:
            status++;
        }
    }
    if (status || optind != argc) {
        fprintf(stderr, "usage: %s [-p port]\n", argv[0]);
        exit(1);
    }
}


void makelistener() {
    struct sockaddr_in r;

    if ((listenfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("socket");
        exit(1);
    }

    int on = 1;
    if (setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, 
               (const char *) &on, sizeof(on)) == -1) {
        perror("setsockopt");
        exit(1);
    }

    memset(&r, '\0', sizeof(r));
    r.sin_family = AF_INET;
    r.sin_addr.s_addr = INADDR_ANY;
    r.sin_port = htons(port);
    if (bind(listenfd, (struct sockaddr *)&r, sizeof(r))) {
        perror("bind");
        exit(1);
    }

    if (listen(listenfd, 5)) {
        perror("listen");
        exit(1);
    }
}

/* call this BEFORE linking the new player in to the list */
int compute_average_pebbles() { 
    struct player *p;
    int i;

    if (playerlist == NULL) {
        return NPEBBLES;
    }

    int nplayers = 0, npebbles = 0;
    for (p = playerlist; p; p = p->next) {
        nplayers++;
        for (i = 0; i < NPITS; i++) {
            npebbles += p->pits[i];
        }
    }
    return ((npebbles - 1) / nplayers / NPITS + 1);  /* round up */
}


int game_is_over() { /* boolean */
    int i;

    if (!playerlist) {
       return 0;  /* we haven't even started yet! */
    }

    for (struct player *p = playerlist; p; p = p->next) {
        int is_all_empty = 1;
        for (i = 0; i < NPITS; i++) {
            if (p->pits[i]) {
                is_all_empty = 0;
            }
        }
        if (is_all_empty) {
            return 1;
        }
    }
    return 0;
}

/* Accept a connection, make this connection a type of struct player
 * and add this client into the fake_playerlist. Return the new client's
 * file descriptor or -1 on error
 */
int accept_connection(int fd) {
    int client_fd = accept(fd, NULL, NULL);
    if (client_fd < 0) {
    	perror("server: accept\n");
	    close(fd);
	    return -1;
    }
    write(client_fd, WELCOME_MESSAGE, strlen(WELCOME_MESSAGE));

    return client_fd;
}

/*
 * Search the first n characters of buf for a newline character (\r or \n).
 * Return the index of the first newline character, or -1 if no network newline is found.
 */
int find_network_newline(const char *buf, int n) {
    int i = 0;
    while(i < n) {
    	if (buf[i] == '\r' || buf[i] == '\n') {
	        return i;	
	    }
	    i++;
    }
    return -1;
}

/* This method is responsible to announce all the players
 * with given message s
 */
void broadcast(char *s) {
    for (struct player *p = playerlist; p; p = p->next) {
        if (p->turn != -1) {
            write(p->fd, s, strlen(s));
        }
    }
}

/* This is a helper method to make the player move
 * This helper method returns 1 if the player gets an extra turn, else 0
 */
int player_move(struct player *p_move, int pit) {
    int *peb_remains = &((p_move->pits)[pit]);
    int *end_pit = &(p_move->pits[6]);
    int current_pit;
    int extra_turn = 0;
    pit++;
    
    while((*peb_remains) > 0) {
        for (;p_move->turn != -1 && pit < 7 && (*peb_remains) > 0; pit++) {
            (p_move->pits)[pit]++;    //increment one pebble in this pit
            (*peb_remains)--;
            current_pit = pit;
        }
        // If this player end his turn by putting a pebble into his own end pit,
        // give an extra turn
        if ((*peb_remains) == 0 && &(p_move->pits[current_pit]) == end_pit){
            extra_turn = 1;
        }
        p_move = p_move->next;
        if (p_move == NULL) {
            p_move = playerlist;
        }
        pit = 0;
    }
    return extra_turn;
}

/* This is a helper method, called when we want to display the game board to everyone
 */
void display_game_board() {
    for (struct player *p = playerlist; p; p = p->next) {
        if (p->turn != -1) {
            char player_state[MAXMESSAGE]; 
            sprintf(player_state, "%s:  [0]%d [1]%d [2]%d [3]%d [4]%d [5]%d [end pit]%d\r\n", 
                p->name, p->pits[0], p->pits[1], p->pits[2], p->pits[3], p->pits[4], p->pits[5], p->pits[6]);
            broadcast(player_state);
        }
    }
}

/* This is the helper function to decide who is the next_player to play the move, we pass in the player who just played a move
 *  return a struct player pointer that points the player who suppose to have the next_turn, returns NULL when no player will have turn 1
 */
struct player *hand_over_turn(struct player *current_player) { 
    // struct player *origin_current = current_player;

    struct player *next_player = current_player->next;     // It's possible this is NULL

    if (next_player == NULL) { // We start from the head
        next_player = playerlist;
        while (next_player->fd != current_player->fd) { // Find the next active player in list
            if (next_player->turn == 0) {
                return next_player;
            }
            next_player = next_player->next;
        }
    }
    else {  // next_player != NULL
        while (next_player->fd != current_player->fd) { // Find the next active player
            if (next_player->turn == 0) {
                return next_player;
            }
            next_player = next_player->next;
            if (next_player == NULL) { // reach the end of playerlist, restart from head
                next_player = playerlist;
            }
        }
    }
    return next_player;
}