#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>
#include <time.h>

#include "LeapC.h"
#include "ExampleConnection.h"

#define RECORD_TIME 10 //Recording Time in seconds
#define MAX_HANDS 2 //Max hands recorded


typedef struct {
    int64_t timestamp;
    int hand_id;
    char hand_type[6]; // "left" or "right"
    float position[3]; //X,Y,Z coordinates
}HandData;

//record motion data
void recordHandData(HandData * handDataArray, int* recordCount, int maxRecords){
    int64_t startTime = LeapGetNow();
    int64_t currentTime = startTime;

    while (currentTime - startTime < RECORD_TIME * 1000000) { //Converts seconds to microseconds since LeapGetNow returns micro seconds
        
        LEAP_TRACKING_EVENT* frame = GetFrame();

        if (frame && *recordCount < maxRecords){ //check if new frame data is available and if there is space in recorded entries
            for (uint32_t h = 0; h < frame->nHands && *recordCount <maxRecords; h++){ //loop through number of detected hands in frakme
                LEAP_HAND* hand = &frame->pHands[h];
                handDataArray[*recordCount].timestamp = frame->info.timestamp; //assign time stamp field of current hand
                handDataArray[*recordCount].hand_id = hand->id; //assign unique ID of current hand
                
                if (hand->type == eLeapHandType_Left){ //need to copy data to be able to store in custom HandData structure created
                    strcpy(handDataArray[*recordCount].hand_type, "left");
                }
                else{
                    strcpy(handDataArray[*recordCount].hand_type, "right");
                }

                handDataArray[*recordCount].position[0] = hand->palm.position.x;
                handDataArray[*recordCount].position[1] = hand->palm.position.y;
                handDataArray[*recordCount].position[2] = hand->palm.position.z;

                (*recordCount)++;


            }
        }

        Sleep(100); //add delay
        currentTime = LeapGetNow(); //update Current time

    } 
}

int main(int argc, char** argv){
    
    //Attempt connection
    LEAP_CONNECTION* connection = OpenConnection();
    
    //Check if connection was established
    if (connection == NULL){
        printf("Failed to open connection to the Leap Motion Controller. \n");
        return EXIT_FAILURE;
    }

    //Try Connection till success
    while (!IsConnected){
        
        printf("Attempting to connect...\n");
        Sleep(250); //Sleep for 250 miliseconds

    }

    //Check connection success or failure
    if (IsConnected){
        printf("Successfully connected to the Leap Motion Controller. \n");

        //memory allocation
        int maxRecords = 1000; 
        HandData* handDataArray = (HandData*)malloc(maxRecords * sizeof(HandData));
        if (!handDataArray){
            printf("Failed to allocate memory for hand data recording.\n");
            CloseConnection();
            DestroyConnection();
            return EXIT_FAILURE;
        }

        int recordCount = 0;
        //Record hand motion data
        recordHandData(handDataArray, &recordCount, maxRecords);

        //Output to terminal
        printf("Recorded Hand Data: \n");
        for (int i = 0; i < recordCount; i++){
            printf("Timestamp: %lli, Hand ID :%d, Type : %s, Position (%.2f, %.2f, %2.f) \n",
            (long long int)handDataArray[i].timestamp, //casting int64_t
            handDataArray[i].hand_id,
            handDataArray[i].hand_type,
            handDataArray[i].position[0],
            handDataArray[i].position[1],
            handDataArray[i].position[2]);


        }
        //Free memory
        free(handDataArray);
    }
    else{
        printf("Failed to connect to the Leap Motion Controller. \n");
    }

    //Close connection and free resources
    CloseConnection();
    DestroyConnection();

    return EXIT_SUCCESS;
    
}
