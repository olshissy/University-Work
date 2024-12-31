#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <mpi.h>
#include <time.h>
#include <unistd.h>
#include <pthread.h>
#include <math.h>
#include <stdbool.h>

#define MSG_REQUEST_NEIGHBOUR 1
#define MSG_BASE_STATION 2
#define MSG_TERMINATION 3

#define NUM_PORTS 5
#define N_DIMS 2
#define MAX_NODES 100

//Global variables used in the processes
int portavailabilty[NUM_PORTS] = {0};
int dims[N_DIMS];
int nodeCoordinates[MAX_NODES][2];
int terminateThreads = false;

//Message stuctures used for sending between processes
typedef struct
{
    int sender_rank;
    int request_type;
} Message;

typedef struct
{
    int closest_nodes[MAX_NODES];
    int request_type;
    int num_closest_nodes;
} NearestNodeMessage;

typedef struct
{
    int sender_rank;
    int request_type;
    int available_ports;
    int node_coords[2];
    int neighbour_ranks[4];
    int neighbour_coords[4][2];
} BaseStationMessage;

int base_station(MPI_Comm world_comm, MPI_Comm comm);
int charging_nodes(MPI_Comm world_comm, MPI_Comm comm);
void *chargingPortThread(void *arg);
int calculate_distance(int first_node_x, int first_node_y, int second_node_x, int second_node_y);

/**
 * Function used to run the full code
*/
int main(int argc, char **argv)
{
    //Set up the MPI for use 
    int rank, size, provided;
    MPI_Comm new_comm;
    MPI_Init_thread(&argc, &argv, MPI_THREAD_MULTIPLE, &provided);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    //Split up the nodes and the base station
    MPI_Comm_split(MPI_COMM_WORLD, rank == size - 1, 0, &new_comm);

    //Run each function depending on the rank 
    if (rank == size - 1) {
        base_station(MPI_COMM_WORLD, new_comm);
    }
    else {
        charging_nodes(MPI_COMM_WORLD, new_comm);
    }

    MPI_Finalize();
    return 0;
}

/**
 * Code that determines base station simulation
*/
int base_station(MPI_Comm world_comm, MPI_Comm comm)
{
    //Set up variables for use in the base station code
    int rank, size, world_size;
    int iteration = 0;
    int numMessages = 0;
    double start_time, end_time;
    MPI_Comm_rank(comm, &rank);
    MPI_Comm_size(comm, &size);
    MPI_Comm_size(world_comm, &world_size);

    //Set up the log file
    FILE *outputFile = fopen("output2.txt", "w");

    if (outputFile == NULL)
    {
        fprintf(stderr, "Error opening the output file.\n");
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    //Set up the lists used 
    int receivedMessages[world_size - 1];

    int allNodes[world_size - 1];

    for (int i = 0; i < world_size - 1; i++)
    {
        allNodes[i] = i;
    }

    //Get the coordinates of all nodes in the program
    MPI_Gather(MPI_IN_PLACE, 0, MPI_DATATYPE_NULL, nodeCoordinates, 2, MPI_INT, world_size - 1, world_comm);

    int terminations_sent = 0; //counter for determining end of program

    //Base station loop
    while (1)
    {
        iteration++;

        //Listen for message from the nodes 
        BaseStationMessage receivedMessage;
        MPI_Status status;
        MPI_Request recv_request;
        MPI_Irecv(&receivedMessage, sizeof(BaseStationMessage), MPI_BYTE, MPI_ANY_SOURCE, MSG_BASE_STATION, world_comm, &recv_request);

        MPI_Wait(&recv_request, &status);

        //If a message is received run the statement
        if (receivedMessage.request_type == MSG_BASE_STATION)
        {
            start_time = MPI_Wtime();

            //50% chance that the base station will send a termination message to the node
            if (rand() % 1 == 0)
            {
                MPI_Request send_request;
                int termination_buf = 0;
                MPI_Isend(&termination_buf, 1, MPI_INT, receivedMessage.sender_rank, MSG_TERMINATION, world_comm, &send_request);
                terminations_sent++;
                printf("Base station terminating node %d for maintenance\n", receivedMessage.sender_rank);
                fflush(stdout);
            }

            numMessages++;
            receivedMessages[receivedMessage.sender_rank] = 1; //Mark the node as having a message sent to base 
            printf("Base station received message from Node %d\n", receivedMessage.sender_rank);
            fflush(stdout);
            
            //Get the current time 
            time_t currentTime;
            struct tm *localTimeInfo;
            char timeString[80]; // Adjust the size as needed

            time(&currentTime);

            currentTime = currentTime + (11 * 3600);
            localTimeInfo = localtime(&currentTime);

            strftime(timeString, sizeof(timeString), "%Y-%m-%d %H:%M:%S", localTimeInfo);
            
            
            int numAdjacentNodes = 0;

            //Write info to log file
            fprintf(outputFile, "\n--------------------------------------------------------------------------------------\n");
            fflush(outputFile);
            fprintf(outputFile, "Iteration : %d\n", iteration);
            fflush(outputFile);
            fprintf(outputFile, "Logged Time : %s\n", timeString);
            fflush(outputFile);
            fprintf(outputFile, "Availability to be considered full : %d\n", receivedMessage.available_ports);
            fflush(outputFile);

            for (int i = 0; i < 4; i++)
            {
                if (receivedMessage.neighbour_ranks[i] >= 0)
                {
                    numAdjacentNodes++;
                }
            }

            fprintf(outputFile, "Number of adjacent nodes : %d\n\n", numAdjacentNodes);
            fflush(outputFile);
            fprintf(outputFile, "Reporting Node     Coords\n");
            fflush(outputFile);
            fprintf(outputFile, "%d                  (%d, %d)\n\n", receivedMessage.sender_rank, receivedMessage.node_coords[0], receivedMessage.node_coords[1]);
            fflush(outputFile);
            fprintf(outputFile, "Adjacent Nodes     Coords\n");
            fflush(outputFile);

            //Write the neighbouring node ranks and coordinates
            for (int i = 0; i < 4; i++)
            {
                if (receivedMessage.neighbour_ranks[i] >= 0)
                {
                    fprintf(outputFile, "%d                  (%d, %d)\n", receivedMessage.neighbour_ranks[i], receivedMessage.neighbour_coords[i][0], receivedMessage.neighbour_coords[i][1]);
                    fflush(outputFile);
                }
            }

            fprintf(outputFile, "\nNearby Nodes     Coords\n");
            fflush(outputFile);
            
            //Find all nearby nodes and write their ranks and coordinates 
            for (int i = 0; i < world_size - 1; i++)
            {
                if (i != receivedMessage.sender_rank) // Exclude the reporting node
                {
                    int dist = calculate_distance(receivedMessage.node_coords[0], receivedMessage.node_coords[1], nodeCoordinates[i][0], nodeCoordinates[i][1]);

                    if (dist == 2) //All nodes that are 2 away from the node (neighbours of neighbours)
                    {
                        fprintf(outputFile, "%d                  (%d, %d)\n", i, nodeCoordinates[i][0], nodeCoordinates[i][1]);
                        fflush(outputFile);
                    }
                }
            }
        }

        int distance = 1000; // buffer to start
        int closestNodes[MAX_NODES];
        int numClosestNodes = 0;

        //Find the available nearest nodes
        for (int i = 0; i < world_size - 1; i++)
        {
            if (!receivedMessages[i]) //If no message is received from the node (indicating its free)
            {
                int dist = calculate_distance(receivedMessage.node_coords[0], receivedMessage.node_coords[1], nodeCoordinates[i][0], nodeCoordinates[i][1]);

                //Find the shortest distance (closest to the reporting node)
                if (dist < distance && dist != 1)
                {
                    numClosestNodes = 0;
                    distance = dist;
                    closestNodes[numClosestNodes++] = i;
                }
                else if (dist == distance)
                {
                    closestNodes[numClosestNodes++] = i;
                }
            }
        }

        //Send this info the node and write it to the log file
        NearestNodeMessage message;
        message.request_type = MSG_BASE_STATION;
        message.num_closest_nodes = numClosestNodes;

        fprintf(outputFile, "\nAvailable stations nearby: ");
        for (int i = 0; i < numClosestNodes; i++)
        {

            message.closest_nodes[i] = closestNodes[i];

            if (i == numClosestNodes - 1)
            {
                fprintf(outputFile, "%d\n", closestNodes[i]);
            }
            else
            {
                fprintf(outputFile, "%d, ", closestNodes[i]);
            }
        }
        if (numClosestNodes == 0)
        {
            fprintf(outputFile, "No nearby nodes available\n");
        }

        MPI_Request send_request;
        MPI_Isend(&message, sizeof(NearestNodeMessage), MPI_BYTE, receivedMessage.sender_rank, MSG_BASE_STATION, world_comm, &send_request);
        numMessages++;

        //Calculate the total time for the interaction and write it to the file
        end_time = MPI_Wtime();
        double iteration_time = end_time - start_time;

        fprintf(outputFile, "Communication Time (seconds): %f\n", iteration_time);
        fprintf(outputFile, "Total Messages sent between reporting node and base station: %d\n", numMessages);

        //Check if all nodes have been terminated and terminate the base station if they have
        if (terminations_sent >= world_size - 1)
        {
            printf("All nodes have been terminated, ending program\n");
            fflush(stdout);
            break;
        }

        sleep(5);
        numMessages = 0;
    }

    fclose(outputFile);
    return 0;
}

/**
 * Function to simulate the charging nodes
*/
int charging_nodes(MPI_Comm world_comm, MPI_Comm comm)
{
    //Define the variables required for the function
    int size, my_rank, reorder, my_cart_rank, ierr, worldSize;
    int coord[N_DIMS];
    int wrap_around[N_DIMS];
    char buf[256];
    MPI_Comm comm2D;

    int exit_loop = 0;

    MPI_Comm_size(world_comm, &worldSize);
    MPI_Comm_size(comm, &size);    // size of the slave communicator
    MPI_Comm_rank(comm, &my_rank); // rank of the slave communicator

    //Get the dimensions of the grid based on number of processors being used 
    dims[0] = dims[1] = 0;
    MPI_Dims_create(size, N_DIMS, dims);

    if (my_rank == 0)
        printf("Slave Rank: %d. Comm Size: %d: Grid Dimension = [%d x %d]\n", my_rank, size, dims[0], dims[1]);
    fflush(stdout);

    /* create cartesian mapping */
    wrap_around[0] = 0;
    wrap_around[1] = 0; /* periodic shift is .false. */
    reorder = 0;
    ierr = 0;
    ierr = MPI_Cart_create(comm, N_DIMS, dims, wrap_around, reorder, &comm2D);

    if (ierr != 0)
        printf("ERROR[%d] creating CART\n", ierr);

    /* find coordinates in the cartesian communicator group */
    MPI_Cart_coords(comm2D, my_rank, N_DIMS, coord);

    /* use cartesian coordinates to find my rank in cartesian
    group*/
    MPI_Cart_rank(comm2D, coord, &my_cart_rank);

    //Set up the threads that represent the ports 
    pthread_t tid[NUM_PORTS];
    int threadNum[NUM_PORTS];

    //Create them and run the thread function below
    for (int i = 0; i < NUM_PORTS; i++)
    {
        threadNum[i] = i;
        pthread_create(&tid[i], NULL, chargingPortThread, &threadNum[i]);
    }

    //Find the ranks of the neighbouring nodes 
    int left, right, up, down;
    MPI_Cart_shift(comm2D, 0, 1, &left, &right);
    MPI_Cart_shift(comm2D, 1, 1, &up, &down);

    int neighbours[4] = {left, right, up, down};
    int neighbour_coords[4][2];

    //Find the coordinates of the neighbouring nodes 
    for (int i = 0; i < 4; i++)
    {
        if (neighbours[i] >= 0)
        {
            int current_coords[2];
            MPI_Cart_coords(comm2D, neighbours[i], N_DIMS, current_coords);
            neighbour_coords[i][0] = current_coords[0];
            neighbour_coords[i][1] = current_coords[1];
        }
        else
        {
            neighbour_coords[i][0] = -1;
            neighbour_coords[i][1] = -1;
        }
    }

    //Send the coordinates of all the nodes so that the base station has access to it 
    int myCoordinates[2];
    myCoordinates[0] = coord[0];
    myCoordinates[1] = coord[1];

    MPI_Gather(myCoordinates, 2, MPI_INT, nodeCoordinates, 2, MPI_INT, worldSize - 1, world_comm);

    //Continue to loop until the exit condition is met 
    while (!exit_loop)
    {
        int fullPorts = 0;

        //Update number of full ports based on the port availability
        for (int i = 0; i < NUM_PORTS; i++)
        {
            fullPorts += portavailabilty[i];
        }

        //If the ports are 80% full
        if (fullPorts >= ceil(NUM_PORTS * 0.8))
        {
            //Set up the required info for messages between neighbours 
            printf("Node %d is almost full, requesting neighbour information\n", my_rank);
            fflush(stdout);
            Message request;
            request.sender_rank = my_rank;
            request.request_type = MSG_REQUEST_NEIGHBOUR;

            Message noNeighbourBuffer;
            noNeighbourBuffer.sender_rank = -1;
            noNeighbourBuffer.request_type = -1;

            Message initialValue;
            initialValue.sender_rank = -2;
            initialValue.request_type = -2;

            Message neighbourStatus[4];

            //Check if the up neighbour exists 
            if (up >= 0)
            {
                //Send the request message to the up neighbour
                MPI_Request send_request;
                MPI_Request recv_request;
                int received = 0;
                double start_time = MPI_Wtime();
                MPI_Isend(&request, sizeof(Message), MPI_BYTE, up, MSG_REQUEST_NEIGHBOUR, comm2D, &send_request);
                
                //Receive the message from the neighbour
                MPI_Irecv(&neighbourStatus[0], sizeof(Message), MPI_BYTE, up, MPI_ANY_TAG, comm2D, &recv_request);

                //If a message is received, the neighbour is also full
                while (!received)
                {
                    MPI_Test(&recv_request, &received, MPI_STATUS_IGNORE);
                    neighbourStatus[0] = initialValue;
                    double elapsed_time = MPI_Wtime() - start_time;

                    //Buffer in case the node has been terminated 
                    if (elapsed_time >= 10)
                    {
                        neighbourStatus[0] = request;
                    }
                }
            }
            
            //Set to a buffer value if no neighbour is present 
            else
            {
                neighbourStatus[0] = noNeighbourBuffer;
            }

            //Check if the down neighbour is present 
            if (down >= 0)
            {
                //Send the request message to the down neighbour
                MPI_Request send_request;
                MPI_Request recv_request;
                double start_time = MPI_Wtime();
                int received = 0;
                MPI_Isend(&request, sizeof(Message), MPI_BYTE, down, MSG_REQUEST_NEIGHBOUR, comm2D, &send_request);
               
                //Receive the message from the neighbour
                MPI_Irecv(&neighbourStatus[0], sizeof(Message), MPI_BYTE, down, MPI_ANY_TAG, comm2D, &recv_request);

                //If a message is received, the neighbour is also full
                while (!received)
                {
                    MPI_Test(&recv_request, &received, MPI_STATUS_IGNORE);
                    double elapsed_time = MPI_Wtime() - start_time;

                    //Buffer in case the node has been terminated 
                    if (elapsed_time >= 10)
                    {
                        neighbourStatus[1] = request;
                    }
                }
            }
            
            //Set to a buffer value if no neighbour is present 
            else
            {
                neighbourStatus[1] = noNeighbourBuffer;
            }

            //Check if the left neighbour is present 
            if (left >= 0)
            {
                //Send the request message to the left neighbour
                MPI_Request send_request;
                MPI_Request recv_request;
                double start_time = MPI_Wtime();
                int received = 0;
                MPI_Isend(&request, sizeof(Message), MPI_BYTE, left, MSG_REQUEST_NEIGHBOUR, comm2D, &send_request);
                
                //Receive the message from the neighbour
                MPI_Irecv(&neighbourStatus[0], sizeof(Message), MPI_BYTE, left, MPI_ANY_TAG, comm2D, &recv_request);

                //If a message is received, the neighbour is also full
                while (!received)
                {
                    MPI_Test(&recv_request, &received, MPI_STATUS_IGNORE);
                    double elapsed_time = MPI_Wtime() - start_time;

                    //Buffer in case the node has been terminated 
                    if (elapsed_time >= 10)
                    {
                        neighbourStatus[2] = request;
                    }
                }
            }
            
            //Set to a buffer value if no neighbour is present 
            else
            {
                neighbourStatus[2] = noNeighbourBuffer;
            }

            //Check if the right neighbour is present 
            if (right >= 0)
            {
                //Send the request message to the right neighbour
                MPI_Request send_request;
                MPI_Request recv_request;
                double start_time = MPI_Wtime();
                int received = 0;
                MPI_Isend(&request, sizeof(Message), MPI_BYTE, right, MSG_REQUEST_NEIGHBOUR, comm2D, &send_request);
                
                //Receive the message from the neighbour
                MPI_Irecv(&neighbourStatus[0], sizeof(Message), MPI_BYTE, right, MPI_ANY_TAG, comm2D, &recv_request);

                //If a message is received, the neighbour is also full
                while (!received)
                {
                    MPI_Test(&recv_request, &received, MPI_STATUS_IGNORE);
                    double elapsed_time = MPI_Wtime() - start_time;

                    //Buffer in case the node has been terminated 
                    if (elapsed_time >= 10)
                    {
                        neighbourStatus[3] = request;
                    }
                }
            }
            
            //Set to a buffer value if no neighbour is present 
            else
            {
                neighbourStatus[3] = noNeighbourBuffer;
            }

            //Check if there are free neighbours 
            int hasAvailableNeighbours = 1;
            int freeNeighbourCount = 0;
            for (int i = 0; i < 4; i++)
            {
                if (neighbourStatus[i].sender_rank == -2)
                {
                    freeNeighbourCount++;
                }
            }

            //If there are no free neighbours, set the neighbour check to 0
            if (freeNeighbourCount == 0)
            {
                hasAvailableNeighbours = 0;
            }

            //If there are no free neighbours 
            if (!hasAvailableNeighbours)
            {
                //Set up the message for sending to the base station
                printf("Node %d has no available neighbours, alerting base station\n", my_rank);
                fflush(stdout);
                BaseStationMessage fullQuad;
                fullQuad.sender_rank = my_rank;
                fullQuad.available_ports = NUM_PORTS - fullPorts;
                fullQuad.request_type = MSG_BASE_STATION;
                fullQuad.node_coords[0] = coord[0], fullQuad.node_coords[1] = coord[1];

                for (int i = 0; i < 4; i++)
                {
                    fullQuad.neighbour_ranks[i] = neighbours[i];
                    fullQuad.neighbour_coords[i][0] = neighbour_coords[i][0];
                    fullQuad.neighbour_coords[i][1] = neighbour_coords[i][1];
                }

                //Send the message to the base station
                MPI_Request send_request;
                MPI_Isend(&fullQuad, sizeof(BaseStationMessage), MPI_BYTE, worldSize - 1, MSG_BASE_STATION, world_comm, &send_request);

                //Receive the nearest available nodes from the base station
                NearestNodeMessage message;
                MPI_Status status;
                MPI_Request recv_request;
                MPI_Irecv(&message, sizeof(NearestNodeMessage), MPI_BYTE, worldSize - 1, MSG_BASE_STATION, world_comm, &recv_request);
                MPI_Wait(&recv_request, &status);

                //Show the nearest available nodes in the terminal
                printf("Node %d received message from base station about available nodes: ", my_rank);
                fflush(stdout);

                for (int i = 0; i < message.num_closest_nodes; i++)
                {
                    int closestRank = message.closest_nodes[i];
                    if (closestRank >= 0)
                    {
                        if (i == message.num_closest_nodes - 1)
                        {
                            printf("%d\n", closestRank);
                            fflush(stdout);
                        }
                        else
                        {
                            printf("%d, ", closestRank);
                            fflush(stdout);
                        }
                    }
                }

                if (message.num_closest_nodes == 0)
                {
                    printf("No available nodes nearby\n");
                    fflush(stdout);
                }

                //Check for termination message from the base station
                MPI_Request termination_request;
                int termination_buffer;
                int termination_received;

                MPI_Irecv(&termination_buffer, 1, MPI_INT, worldSize - 1, MSG_TERMINATION, world_comm, &termination_request);
                MPI_Test(&termination_request, &termination_received, MPI_STATUS_IGNORE);

                //If a message is received set the exit condition to 1 and the thread condition to true
                if (termination_received)
                {
                    exit_loop = 1;
                    terminateThreads = true;
                    printf("Node %d has received termination message from base station. Exiting\n", my_rank);
                    fflush(stdout);
                }
            }
        }

        sleep(5);
    }

    //Join all the threads 
    for (int i = 0; i < NUM_PORTS; i++)
    {
        pthread_join(tid[i], NULL);
    }

    MPI_Comm_free(&comm2D);
    return 0;
}

/**
 * Thread function for simulating ports 
*/
void *chargingPortThread(void *arg)
{
    int rank = *((int *)arg);

    //While the condition is false, randomly update the port value
    while (!terminateThreads)
    {
        int availability = rand() % 2;

        portavailabilty[rank] = availability;

        sleep(5);
    }

    return NULL;
}

/**
 * Function to calculate distance between two nodes
*/
int calculate_distance(int first_node_x, int first_node_y, int second_node_x, int second_node_y)
{
    //Use the distance formula to calculate the distance
    double x_values = pow((second_node_x - first_node_x), 2);
    double y_values = pow((second_node_y - first_node_y), 2);

    double distance = sqrt(x_values + y_values);

    //If the distance is root 2 (indicating diagonal), treat it as 2
    if (distance == sqrt(2))
    {
        distance = 2;
    }

    //If the distance is not a whole number, set to a buffer value
    else if (distance != (int)distance)
    {
        distance = 100;
    }

    return distance;
}