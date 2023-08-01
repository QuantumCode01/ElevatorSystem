from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status


#function to open the door
def door_open(closest_elevator,requested_floor):
    if closest_elevator.door == "Close":
        closest_elevator.door="Open"
        return(f"{closest_elevator.elevator_id}: Opening door for person to enter, on floor: {requested_floor}")
    
elevators = elevator.objects.all()


#fucntion to find the closest elevator and send it to the requested floor
def find_closest_elevator(requested_floor, elevators=elevators):
    #elevators those are not busy
    available_elevators = [elevator for elevator in elevators if not elevator.is_busy]
   
    
    if requested_floor == 1:
        # If the requested floor is 1, prioritize elevators already at floor 1
        closest_elevator = next((elevator for elevator in available_elevators if elevator.current_floor == 1))
    else:
        #elevator which is closest to the requested floor
        closest_elevator = min(available_elevators, key=lambda elevator: (abs(elevator.current_floor - requested_floor)))
         
    if closest_elevator:   
             
        # update elevator status to busy   
        closest_elevator.is_busy = True
        closest_elevator.save()
        
        # Send the elevator to the requested floor and update elevator status
        #Checks elevator floor is equal to requested floor or not 
        while closest_elevator.current_floor!=requested_floor:
            if closest_elevator.current_floor < requested_floor:
                # elevator floor increases one by one(moves up)
                closest_elevator.current_floor += 1
            else:
                #elevator floor decrease one by one(moves down)
                closest_elevator.current_floor -= 1
            print(f"{closest_elevator} moving to floor {closest_elevator.current_floor}...")
            
            
            
        print(f"Sending elevator {closest_elevator.elevator_id} to floor {requested_floor}")
        #opening door of elevator for person
        dooropen=door_open(closest_elevator,requested_floor)
        closest_elevator.save()
        #returns message to show.
        return (f"Sending elevator {closest_elevator.elevator_id} to floor {requested_floor}",closest_elevator,dooropen)
    else:
        return ("All elevators are busy. Please wait for an available elevator.")



#func to move the closest elevator to destination floor
def move_to_destinationfloor(assigned_elevator, destination_floor):
        if destination_floor < 1:
            return("Invalid floor.")
        
        #check if destination_floor is equal to the current floor of elevator
        # based on that elevator moves up or down to reach the destination floor
        while assigned_elevator.current_floor != destination_floor:
            # checks if elevator floor is less then destination floor
            if assigned_elevator.current_floor < destination_floor:
                #elevator floor increases one by one
              assigned_elevator.current_floor += 1
            else:
                #elevator floor decreases one by one till floor is same as destination floor
               assigned_elevator.current_floor -= 1

            print(f"assigned_elevator moving to floor {assigned_elevator.current_floor}...")

        print(f"Assigned elevator: {assigned_elevator.elevator_id} has reached the destination floor: {destination_floor}.")
        assigned_elevator.is_busy=False
        
        #Closing door of elevator after person leaves the elevator
        assigned_elevator.door="Close"
        assigned_elevator.save()
        return (f"Assigned elevator: {assigned_elevator.elevator_id} has reached the destination floor: {destination_floor}.")

        


# Create, Update, Delete and Show the details of elevator
class ElevatorAPI(APIView): 
    
    #To get the details of elevators in the elevator system.
   
    def get(self, request,pk=None, format=None):
        id =pk
        #Show details of elevator whose id is provided
        if id is not None:
            data =elevator.objects.get(id=id)
            serializer=ElevatorSerializer(data)
            return Response(serializer.data)
        
        #If no id is given then details of all elevator together is shown
        data=elevator.objects.all()
        serializer=ElevatorSerializer(data,many=True)
        return Response(serializer.data)

    #Create the elavator 
    def post(self,request,format=None):

            serializer=ElevatorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                res={"msg":"Data Created"}
                return Response(res,status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Update the details of a paticular elevator completely
    def put(self, request, pk,format=None):
            id=pk
            dt=elevator.objects.get(id=id)
            serializer=ElevatorSerializer(dt,data=request.data)
            if serializer.is_valid():
                serializer.save()
                res={"msg":"Data Updated"}
                
                return Response(res,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    #Partially update the details of a particular elevator
    def patch(self,request,pk,format=None):
            id=pk
            dt=elevator.objects.get(id=id)
            serializer=ElevatorSerializer(dt,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                res={"msg":"Data Updated"}
                
                return Response(res,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    #Delete a particular elevator  
    def delete(self, request, pk, format=None):
            id=pk
            dt=elevator.objects.get(id=id)
            dt.delete()
            res={"msg":"Data Deleted"}
            return Response(res,status=status.HTTP_200_OK)
        
# Create, Update, Delete and Show the details of Person
class PersonAPI(APIView):   
    
     #To get the details of Person who requested the elevator.
    def get(self, request,pk=None, format=None):
        id =pk
        #Show details of Person whose id is provided
        if id is not None:
            data =Person.objects.get(id=id)
            serializer=PersonSerializer(data)
            return Response(serializer.data)
        #If no id is given then details of all Persons together is shown
        data=Person.objects.filter(elevator__isnull=False)
        serializer=PersonSerializer(data,many=True)
        return Response(serializer.data)
    
    
    #Create the Person  
    def post(self,request,format=None):
            requested_floor=request.data.get("requesting_floor")
            serializer=PersonSerializer(data=request.data)
     
            if serializer.is_valid():
                serializer.save()
                
                # Requested floor is passed as an argument to the function.
                # This Function assignes the closest elevator to the person based on requested floor and moves the elevator to the requested floor..
                # and also opens the door of elevator once it reached the requesting floor
                # and also returns the closest elevator's details.
                # Moves the elevator to the requested floor.
                closest_elevator_assign,closest_elevator,dooropen = find_closest_elevator(requested_floor)
                
                dt=Person.objects.get(requesting_floor=requested_floor)

                #closest elevator is assigned to the Person.
                dt.elevator=closest_elevator
                dt.save()
             
                res={"msg":"Data Created","message1":closest_elevator_assign,"message2":dooropen,"message3":"Person Enters the elevator"}
                return Response(res,status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #Partially update the details of a particular elevator
    #Enter destination_floor
    # So that assigned elevator moves to the destination floor
    def patch(self, request,pk,format=None):
        id=pk
        person=Person.objects.get(id=id)
        destination_floor=request.data.get("destination_floor")
        assigned_elevator=elevator.objects.get(id=person.elevator_id)
        serializer=PersonSerializer(person,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            # This function takes the entered destination floor and moves the 
            #assigned elevator which is at the requested floor to the destination floor and after reaching 
            # destination floor it closes the door of elevator and marks is_busy=False
            message=move_to_destinationfloor(assigned_elevator,destination_floor)
            # Once function is excuted Person details are deleted
            person.delete()
            res={"msg":"Destination floor Saved","message":message}
            return Response(res,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
    # Delete the details of Person            
    def delete(self, request, pk, format=None):
        id=pk
        dt=Person.objects.get(id=id)
        dt.delete()
        res={"msg":"Data Deleted"}
        return Response(res,status=status.HTTP_200_OK)
        
        

    