/*
* @file botTemplate.cpp
* @author Arun Tejasvi Chaganty <arunchaganty@gmail.com>
* @date 2010-02-04
* Template for users to create their own bots
*/
#include "Othello.h"
#include "OthelloBoard.h"
#include "OthelloPlayer.h"
#include <cstdlib>
using namespace std;
using namespace Desdemona;
#include <time.h>

time_t start_time;
time_t heuristic_time;


class MyBot: public OthelloPlayer
{
    public:
        /**
         * Initialisation routines here
         * This could do anything from open up a cache of "best moves" to
         * spawning a background processing thread. 
         */
        MyBot( Turn turn );

        bool isBlackTurn = true;
        time_t heur_t;
        time_t heur_endt;

        /**
         * Play something 
         */
        virtual Move play( const OthelloBoard& board );
        virtual int Min_Max(OthelloBoard &board, Turn turn, int depth, Move move);
        virtual int Heuristic_Move(OthelloBoard &board, Turn turn, int depth, Move move);
        //virtual int Ply_Search(OthelloBoard &board, Turn turn, int depth, Move move);
    private:
};

MyBot::MyBot( Turn turn )
    : OthelloPlayer( turn )
{
}

Move MyBot::play( const OthelloBoard& board )
{
    time(&start_time);
    //cout << "turn is " << turn << "\n";
    list<Move> moves = board.getValidMoves( turn );

    Move bestmove = moves.front();

    int best_value;

    if (this->turn == 1){
        best_value = -111111111;
    }else{
        best_value = 11111111;
    }

    /*
            MinMax Algo to get best move here
    */

   for (Move nextmove : moves){
           
       OthelloBoard cardboard = OthelloBoard(board);

       int Heuristic = Min_Max(cardboard,this->turn,4,nextmove); //Algo(nextmove);

       time(&this->heur_t);

       if (difftime(this->heur_t,start_time)>1.6){
           Heuristic = -12345;
       }

       if (Heuristic == -12345){
           return bestmove;
       }

       if (Heuristic > best_value && turn == 1){
           bestmove = nextmove;
           best_value = Heuristic;
       }

        if (Heuristic < best_value && turn == 2){
           bestmove = nextmove;
           best_value = Heuristic;
       }



   }
    return bestmove;
}

int MyBot::Min_Max(OthelloBoard &board, Turn turn, int depth, Move move){

    time(&heuristic_time);

    if (difftime(heuristic_time,start_time)>1){
        return -12345;
    }


    if (depth == 0){
        return MyBot::Heuristic_Move(board,turn,depth,move);
    }

    OthelloBoard cardboard = OthelloBoard(board);
    cardboard.makeMove(turn,move);    
    list<Move> moves = cardboard.getValidMoves(other(turn));
    Move bestmove = moves.front();
    int bestvalue = (turn == this->turn) ? 12345 : -12345;
    if (moves.size() == 0){
        return cardboard.getBlackCount() - cardboard.getRedCount();
    }

    if (turn == this->turn){ // if bots turn make max move and return best of mins turn
        for (Move nextmove : moves){
        
        time(&heuristic_time);

        if (difftime(heuristic_time,start_time)>1){
            continue;
        }
        
        int Heuristic = MyBot::Min_Max(cardboard,other(turn),depth-1,nextmove);
        if (Heuristic<bestvalue){
            bestvalue = Heuristic;
            bestmove = nextmove;
        }
        }
    }

    if (turn == other(this->turn)){  // if not bots turn make min move and return best of maxs turn
        for (Move nextmove : moves){

            time(&heuristic_time);

            if (difftime(heuristic_time,start_time)>1){
                continue;
            }

        int Heuristic = MyBot::Min_Max(cardboard,other(turn),depth-1,nextmove);
        if (Heuristic>bestvalue){
            bestvalue = Heuristic;
            bestmove = nextmove;
        }
        }
    }    

    time(&heuristic_time);

    if (difftime(heuristic_time,start_time)>1){
        return -12345;
    }

    return MyBot::Min_Max(cardboard,other(turn),depth-1,bestmove);
}

// Returns Heuristic if turn,move is made;
//
int MyBot::Heuristic_Move(OthelloBoard &board, Turn turn, int depth, Move move){ 
    OthelloBoard cardBoard = OthelloBoard(board);
    cardBoard.makeMove(turn,move);
    return board.getBlackCount() - board.getRedCount();
}

// The following lines are _very_ important to create a bot module for Desdemona

extern "C" {
    OthelloPlayer* createBot( Turn turn )
    {
        return new MyBot( turn );
    }

    void destroyBot( OthelloPlayer* bot )
    {
        delete bot;
    }
}


