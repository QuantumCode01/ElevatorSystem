# ElevatorSystem - Django Rest Framework
# Problem Solved:
- An elevator system, which can be initialized with N elevators and maintains the elevator states as well.

- Each elevator has below capabilities:
   - Move Up and Down
   - Open and Close the Door
   - Start and Stop Running
   - Display Current Status
   -  Decide whether to move up or down, based on a list of requests from users.
  
- The elevator System takes care of:
   - Decides which lift to associate with which floor.
   - Marks which elevator is available or busy.
   - Can mark which elevator is operational and which is not.

# Assumptions:
   - The number of elevators in the system will be defined by the API to initialize the elevator system
   - The elevator System has got only one button per floor.
   - So if there are a total of 5 floors, there will be 5 buttons per floor.
   - Note that this doesn't mimic the real world when you would have a total of 10 buttons for 5 floors (one for up and one for down)
   - **After entering the requested floor, the elevator closest to that floor will move either up or down to reach it.After reaching the requested floor door of the elevator gets open. Assume the person enters the elevator and enters the destination floor.**
   - **Once the destination floor is entered, the elevator will move in the appropriate direction to reach it. Once the elevator reaches the destination floor.The elevator door opens and assume person comes out of the elevator. And the Person's record is deleted.**
   - The system has to assign the most optimal available elevator to the user according to the requested floor.

# APIs required:
 - Initialise the elevator system to create `n` elevators in the system
 - Fetch details for a given elevator
 - Fetch details of all elevator
 - Create the Person that enters the requested floor.
 - Fetch details of the Person with the assigned elevator.
 - Enter the destination floor to make the elevator move toward it

    | Method | URL | Description |
    | :---         |     :---:      |     :---: |
    | `GET`   |  http://127.0.0.1:8000/api/elevator/    | Retrieve details of all elevators created    |
    | `GET`   |  http://127.0.0.1:8000/api/elevator/1   | Retrieve details of elevator whose id=1   |
    | `POST`   |http://127.0.0.1:8000/api/elevator/| Create an elevator by passing elevator_id, current_floor,operational, is_busy, door| 
    | `POST`   | http://127.0.0.1:8000/api/Person/ |Create the Person's record by passing requesting_floor and closest elevator is assigned to the person|
    | `GET`   | http://127.0.0.1:8000/api/Person/| Retrieve details of all Persons with assigned elevator   |
    | `GET`   | http://127.0.0.1:8000/api/Person/6| Retrieve details of individual Person with assigned elevator having id=6   |
    | `PATCH`   |http://127.0.0.1:8000/api/Person/6/    | Enter the destination_floor for the person with id=6 so that elevator moves towards the destination floor     |

# Headers:
  |Header|Value|
  |:---| ---:|
  |`Accept`|`application/json`|