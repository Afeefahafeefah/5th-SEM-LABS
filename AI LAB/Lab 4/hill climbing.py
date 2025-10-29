from random import randint

N =4


def configureRandomly(board, state):

 
    for i in range(N):

       
        state[i] = randint(0, 100000) % N;

        
        board[state[i]][i] = 1;
   

def printBoard(board):
    
    for i in range(N):
        print(*board[i])


def printState( state):
    print(*state)
    

def compareStates(state1, state2):


    for i in range(N):
        if (state1[i] != state2[i]):
            return False;
    
    return True;


def fill(board, value):
    
    for i in range(N):
        for j in range(N):
            board[i][j] = value;
        

def calculateObjective( board, state):

    attacking = 0;

    
    for i in range(N):

        
        row = state[i]
        col = i - 1;
        while (col >= 0 and board[row][col] != 1) :
            col -= 1
        
        if (col >= 0 and board[row][col] == 1) :
            attacking += 1;
        
       
        row = state[i]
        col = i + 1;
        while (col < N and board[row][col] != 1):
            col += 1;
        
        if (col < N and board[row][col] == 1) :
            attacking += 1;
        
        row = state[i] - 1
        col = i - 1;
        while (col >= 0 and row >= 0 and board[row][col] != 1) :
            col-= 1;
            row-= 1;
        
        if (col >= 0 and row >= 0  and board[row][col] == 1) :
            attacking+= 1;
        
        
        row = state[i] + 1
        col = i + 1;
        while (col < N and row < N  and board[row][col] != 1) :
            col+= 1;
            row+= 1;
        
        if (col < N and row < N and board[row][col] == 1) :
            attacking += 1;
        
      
        row = state[i] + 1
        col = i - 1;
        while (col >= 0 and row < N  and board[row][col] != 1) :
            col -= 1;
            row += 1;
        
        if (col >= 0 and row < N and board[row][col] == 1) :
            attacking += 1;
        
        
        row = state[i] - 1
        col = i + 1;
        while (col < N and row >= 0  and board[row][col] != 1) :
            col += 1;
            row -= 1;
        
        if (col < N and row >= 0 and board[row][col] == 1) :
            attacking += 1;
        
   
    return int(attacking / 2);


def generateBoard( board, state):
    fill(board, 0);
    for i in range(N):
        board[state[i]][i] = 1;
    

def copyState( state1, state2):

    for i in range(N):
        state1[i] = state2[i];
    

def getNeighbour(board, state):

   
    opBoard = [[0 for _ in range(N)] for _ in range(N)]
    opState = [0 for _ in range(N)]

    copyState(opState, state);
    generateBoard(opBoard, opState);

    
    opObjective  = calculateObjective(opBoard, opState);

    
    NeighbourBoard = [[0 for _ in range(N)] for _ in range(N)]
    
    NeighbourState = [0 for _ in range(N)]
    copyState(NeighbourState, state);
    generateBoard(NeighbourBoard, NeighbourState);

   
    for i in range(N):
        for j in range(N):

           
            if (j != state[i]) :

               
                NeighbourState[i] = j;
                NeighbourBoard[NeighbourState[i]][i] = 1;
                NeighbourBoard[state[i]][i] = 0;

              
                temp = calculateObjective( NeighbourBoard, NeighbourState);

             

                if (temp <= opObjective) :
                    opObjective = temp;
                    copyState(opState, NeighbourState);
                    generateBoard(opBoard, opState);
                
               
                NeighbourBoard[NeighbourState[i]][i] = 0;
                NeighbourState[i] = state[i];
                NeighbourBoard[state[i]][i] = 1;
            
   
    copyState(state, opState);
    fill(board, 0);
    generateBoard(board, state);

def hillClimbing(board, state):

  

    neighbourBoard = [[0 for _ in range(N)] for _ in range(N)]
    neighbourState = [0 for _ in range(N)]

    copyState(neighbourState, state);
    generateBoard(neighbourBoard, neighbourState);
    
    while True:

       

        copyState(state, neighbourState);
        generateBoard(board, state);

   

        getNeighbour(neighbourBoard, neighbourState);

        if (compareStates(state, neighbourState)) :

     

            printBoard(board);
            break;
        
        elif (calculateObjective(board, state) == calculateObjective( neighbourBoard,neighbourState)):

 
            neighbourState[randint(0, 100000) % N]  = randint(0, 100000) % N;
            generateBoard(neighbourBoard, neighbourState);

state = [0] * N
board = [[0 for _ in range(N)] for _ in range(N)]

configureRandomly(board, state);

hillClimbing(board, state);
