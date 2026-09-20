from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Autonomous Mission Commander")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173","http://localhost:5174","http://127.0.0.1:5174","http://localhost:5175","http://127.0.0.1:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mission_state = {
    "mission_id":"MISSION-001",
    "battery":85,
    "fuel":72,
    "communication":True,
    "navigation_uncertainty":10,
    "current_location":"ORBIT-A",
    "mission_objective":"MARS_SOIL_ANALYSIS",
    "experiment_status":"ACTIVE",
    "actions":[],
    "log":[]
}

PRIORITY = {
    "EMERGENCY_ABORT":5,
    "BATTERY_FAILURE":4,
    "FUEL_LEAK":3,
    "COMMUNICATION_FAILURE":2,
    "NAVIGATION_FAILURE":1
}

class MissionEvent(BaseModel):
    event:str

@app.get("/")
def home():
    return {"message":"Mission Commander is online"}

@app.get("/mission/state")
def mission_state_api():
    return mission_state

@app.get("/mission/log")
def mission_log():
    return {
        "mission_id":mission_state["mission_id"],
        "event_count":len(mission_state["log"]),
        "timeline":mission_state["log"]
    }

@app.post("/mission/event")
def mission_event(event:MissionEvent):

    mission_state["log"].append(event.event)

    if event.event=="BATTERY_FAILURE":
        mission_state["battery"]=20
        mission_state["experiment_status"]="PAUSED"
        for a in ["ENTER_LOW_POWER_MODE","PAUSE_EXPERIMENT"]:
            if a not in mission_state["actions"]:
                mission_state["actions"].append(a)

    elif event.event=="NAVIGATION_FAILURE":
        mission_state["navigation_uncertainty"]=50
        if "MODIFY_TRAJECTORY" not in mission_state["actions"]:
            mission_state["actions"].append("MODIFY_TRAJECTORY")

    elif event.event=="COMMUNICATION_FAILURE":
        mission_state["communication"]=False
        if "RESTORE_COMMUNICATION" not in mission_state["actions"]:
            mission_state["actions"].append("RESTORE_COMMUNICATION")

    elif event.event=="COMMUNICATION_RESTORED":
        mission_state["communication"]=True

    elif event.event=="FUEL_LEAK":
        mission_state["fuel"]=40
        if "SEAL_FUEL_LEAK" not in mission_state["actions"]:
            mission_state["actions"].append("SEAL_FUEL_LEAK")

    elif event.event=="FUEL_LEAK_SEALED":
        mission_state["fuel"]=70

    elif event.event=="EMERGENCY_ABORT":
        mission_state["experiment_status"]="ABORTED"
        mission_state["actions"]=["RETURN_TO_SAFE_ORBIT","ABORT_MISSION"]

    return {"event_received":event.event,"mission_state":mission_state}

@app.post("/mission/decide")
def mission_decision():

    actions=[]
    reasons=[]
    priority=0

    if mission_state["experiment_status"]=="ABORTED":
        priority=5
        actions=["RETURN_TO_SAFE_ORBIT","ABORT_MISSION"]
        reasons=["Mission aborted"]

    else:

        if mission_state["battery"]<=20:
            priority=max(priority,PRIORITY["BATTERY_FAILURE"])
            actions.extend(["ENTER_LOW_POWER_MODE","PAUSE_EXPERIMENT"])
            reasons.append("Battery critically low")

        if mission_state["fuel"]<=40:
            priority=max(priority,PRIORITY["FUEL_LEAK"])
            actions.append("SEAL_FUEL_LEAK")
            reasons.append("Fuel leak detected")

        if not mission_state["communication"]:
            priority=max(priority,PRIORITY["COMMUNICATION_FAILURE"])
            actions.append("RESTORE_COMMUNICATION")
            reasons.append("Communication unavailable")

        if mission_state["navigation_uncertainty"]>=30:
            priority=max(priority,PRIORITY["NAVIGATION_FAILURE"])
            actions.append("MODIFY_TRAJECTORY")
            reasons.append("Navigation uncertainty high")

    if priority==0:
        return {
            "decision":"CONTINUE_MISSION",
            "priority":0,
            "actions":[],
            "reasoning":["Mission conditions are within normal limits"]
        }

    return {
        "decision":"RECOVERY_MODE",
        "priority":priority,
        "actions":actions,
        "reasoning":reasons
    }