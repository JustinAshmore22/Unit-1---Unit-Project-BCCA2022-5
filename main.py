from dataclasses import dataclass
import time
import sys
import select

timeout = 5
start = time.time

scp_desc = f"""


======================================================================
SCPs are possible anomolies/creatures/items that you may encounter in the facility.  They are extremely dangerous.  This is the information you are allowed on them:
_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
"""

scp_261_desc = """
SCP-261: "The Vending Machine."

Object Class: Safe

This item appears to be a standard coffee vending machine, the only noticeable difference being an entry touchpad with buttons corresponding to an English QWERTY keyboard.vUpon depositing fifty cents US currency into the coin slot,the user is prompted to enter the name of any liquid using the touchpad. Upon doing so, a standard 12-ounce paper drinking cup is placed and the liquid indicated is poured. Ninety-seven initial test runs were performed (including requests for water, coffee, beer, and soda, non-consumable liquids such as sulfuric acid, wiper fluid, and motor oil, as well as substances that do not usually exist in liquid state, such as nitrogen, iron and glass) and each one returned a success. Test runs with solid materials such as diamond have failed, however, as it appears that SCP-294 can only deliver substances that can exist in liquid state.

Containment Procedures: N/A

--------------------------------------------------------------------
"""

scp_087_desc = """SCP-087: "The Staircase."

Object Class: Euclid

An endless staircase going down that contains a humanoid figure, SCP-087-1. The constant sound of crying can be heard deep within SCP-087.

Containment Procedures: Do NOT enter the staircase.  It is unknown what will happen if you do so.  SCP-087 is subject to further testing.  Doctor [REDACTED] is currently seeking approval for another exploration team.

--------------------------------------------------------------------
"""

scp_173_desc = """SCP-173: "Billy."

Object Class: Euclid

A scultpure constructed out of condcrete. It is capable of moving at high speeds and will kill by either snapping at the base of the skull or strangulation. However, it is incapable of moving while in the direct line of sight of a person.

Containment Procedures:  No more than 3 personelle may attempt contact with SCP-173 at any given moment.  2 personelle must keep direct contact with SCP-173 at all times and notify others when they have the urge to blink.

---------------------------------------------------------------------
"""

scp_993_desc = """SCP-993: "Bobble The Clown"

Object Class: Safe

is a children's television program entitled 'Bobble the Clown'. In Bobble the clown- causes anyone over the age of ten to pass out upon viewing it.

Containment Procedures:  Any airing of SCP-993 must be intercepted and blocked from public viewing.  Any watchers of SCP-173 must be under the age of 10 and to be dosed with a Class A Amnesiac after viewing.

---------------------------------------------------------------------
"""

scp_096_desc = """SCP-096: 

Object Class: Euclid

A tall, pale, humanoid that will kill anyone or anything that sees its face. It is indestructible and unstoppable when enraged.

Containment Proceedure:  Do not look at it's face.  Do not look at a picture or drawing of its face.  Do not look at a video of its face.  Viewing the face of SCP-096 will result in imminent death of the viewer.

---------------------------------------------------------------------
"""

scp_999_desc = """SCP-999:

Object Class: Safe

An adorable orange-colored slime creature, which cures anyone-anything in pain. It weights about 120lbs with a consistency similar to that of peanut butter. Is the size of a large beanbag chair.

Containment Proceedures: SCP-999 is allowed to freely roam the facility should it desire to, but otherwise must stay in its pen either between 8PM-9PM for sleeping, or during emergency lockdowns for its own safety. Subject is not allowed out of its pen at night or off facility grounds at any time. Pen is to be kept clean and food replaced twice daily. All personnel are allowed inside SCP-999’s holding area, but only if they are not assigned to other tasks at the time, or if they are on break. Subject is to be played with when bored and spoken to in a calm, non-threatening tone.

======================================================================"""  #Healing time is not instant

cl_desc = f"""
======================================================================
Clearance Levels give you access to certain areas of the SCP Facility.  These are the possible levels of clearance:
_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-"""

dc_desc = f"""
This is the lowest clearance level available.
----------------------------------------------------------------------"""

c1_desc = f"""
A RED card with a large 1 in the middle of it. This can be used to access level 1 areas.
----------------------------------------------------------------------"""
c2_desc = f"""
An ORANGE card with a large 2 in the middle of it. This can be used to access level 2 areas.
----------------------------------------------------------------------"""
c3_desc = f"""
A YELLOW card with a large 3 in the middle of it. This can be used to access level 3 areas.
----------------------------------------------------------------------"""
c4_desc = f"""
A GREEN card with a large 4 in the middle of it. This can be used to access level 4 areas.
----------------------------------------------------------------------"""
c5_desc = f"""
A BLUE card with a large 5 in the middle of it. This can be used to access level 5 areas.
----------------------------------------------------------------------"""
c6_desc = f"""
A PURPLE card with a large 6 in the middle of it. This can be used to access ALL areas.
======================================================================"""

welcomemessage = "Welcome to the SCP Foundation Site [REDACTED]"

sg_em = "You do not have authorization to enter!"
startlocation = "Level 0: Hallway"

l0_hallway_info = "A long hallway leading to a steel gate. *Looks safe to move ahead to the steel gate, You also notice a RED card on the floor, there is a large 1 plastered in the middle of it* \n[Level 0: Steel Gate] - [Level 0: Card Pick-Up] - [Q]"

l0_steelgate_info = "Enter this gate to go inside to level 1. \n[Level 1: Hallway 1] - [Level 0: Card Pick-Up] - [Level 0: Hallway] - [Q]"

l0_cardpickup_info = "\n[Level 0: Hallway] - [Level 0: Steel Gate]"

l1_cardpickup_info = "\n[Level 1: Supervisor Room] - [Level 1: Meeting Room]"

l1_hw1_info = "Welcome to level 1. You have entered the SCP Foundation. Now that you have entered the building you notice a horrid smell. This hallway leads to the Meeting Room and hallway 7. Go right to hallway 2 or left to hallway 3\n[Level 1: Meeting Room] - [Level 1: Hallway 7] - [Level 1: Hallway 2] - [Level 1: Hallway 3]"

l1_hw2_info = "Down this hallway is the breakroom and hallway 4.\n[Level 1: Breakroom] - [Level 1: Hallway 1] - [Level 1: Hallway 4]"

l1_hw3_info = "Down this hallway is the office and another hallway leading up. On the floor you knowtice a poster of a clown(coincidence? maybe.)\n[Level 1: Office] - [Level 1: Hallway 5] - [Level 1: Hallway 1]"

l1_hw4_info = "Going down this hallway leads to the stair case, a hallway going left and a open hallway that goes to all other hallways.\n[Level 1: Steel Gate] - [Level 1: Hallway 2] - [Level 1: Hallway 6] - [Level 1: Hallway 7]"

l1_hw5_info = "This hallway is very bland, but has some damage to the walls such as scratchs and blood. This hallway leads to hallway 7.\n[Level 1: Hallway 3] - [Level 1: Hallway 7]"

l1_hw6_info = "As you travel down this hallway you realize that it is a deadend. At the end of this hallway is a very creepy note that says 'TURN BACK NOW!!'\n[Level 1: Hallway 4]"

l1_hw7_info = "This hallway leads to all the other hallways. In this hallway the cealing is caved in some and mold on the floor. At the very end of this hallway there is a steelgate leading to the next level.\n[Level 1: Hallway 5] - [Level 1: Hallway 1] - [Level 1: Hallway 4] - [Level 1: Meeting Room] - [Level 1: Steel Gate]"

l1_breakroom_info = "Inside the breakroom you notice blood on the walls and a dead body near a table to the right. As you continue to look around you see a vending machine. Do you attempt to buy a drink?\n[Level 1: Hallway 2] - [Level 1: Vending Machine]"

l1_office_info = "You have entered the office. Inside the office you find a mess of scientific files and papers laying all around. A desk with a computer that is to damaged to use. A message in blood that reads'GET OUT NOW'. To the left their is a very dusty window that you can faintly see out of You search the office for a clearance card but do not find one.\n[Level 1: Hallway 3] - [Level 1: Health Pack]"

l1_meetroom_info = "You have entered the meeting room. In the middle of the room their is a long desk with chairs surrounding it. In those chairs you see reminance, Suit coats and a lab coat, of people being their. You walk closer to the lab coat and see a person's remains. You look up to find on the wall a white board with scientific notes that have been marked out and a date that reads 'Sept 10, 2015.' You see that their is a supervisor room, but it is locked. You look around for a keycard but do not find one, but you do find a key for the supervisor room.\n[Level 1: Supervisor Room] - [Level 1: Hallway 1] - [Level 1: Hallway 7]"

l1_svroom_info = "You have entered the supervisor room. The room is dusty but suprisedly clean. Could it be because it was locked?. Their is pictures and other things hanging on the wall. Next to a paperwork and pictures on a desk. You also notice an ORANGE card on the desk, there is a large 2 plastered in the middle of it*\n[Level 1: Card Pick-Up] - [Level 1: Meeting Room]"

l1_vendingmachine_info = "[Level 1: Breakroom] - [Level 1: Hallway 2]"

# l1_clcheck = ""

l1_steelgate_info = "Enter this gate to go up the stairs to level 2.\n[Level 1: Hallway 7] - [Level 2: Hall]"

#LEVEL 2
l2_hall_info = "Welcome to level 2. This floor is very worn down and has a pungent odor. Human remains? Blood? Maybe? On this floor you can go down to the Men's bathroom or Women's bathroom or travel to the main hall.\n[Level 2: Main Hallway] - [Level 2: Men's Bathroom] - [Level 2: Womens's Bathroom]"

l2_mb_desc = "You have entered the men's bathroom. This bathroom is very unsantitary. Nasty water in the toilet that is brown. You do not even look around for the keycard.\n[Level 2: Hall]"

l2_wb_desc = "You have entered the women's bathroom. The bathroom is not as dirty as you would have imagined. You search the bathroom and find soap, but no keycard.\n[Level 2: Hall]"

l2_mainhall_desc = "Walking down this hallway you find the steel gate. There is a hallway, leading to a surveillance room and an office, to the right and two rooms by the steel gate. Their is bloody handprints on the floor.\n[Level 2: Hall] - [Level 2: Hallway 2] - [Level 2: Supply Closet] - [Level 2: Utility Room] - [Level 2: Steel Gate]"

l2_supplycloset_desc = "You have entered the supply closet to find that there is not much in the room to that is still useful. You search the supply closet and find one semi-clean rag, but no keycard\n[Level 2: Main Hallway]"

l2_utilroom_desc = "Entering the utility room you see clean and dirty labcoats. One lab coat has blood all over it. There is a washing machine and dryer in this room. You search around and find on top of the dryer a YELLOW, there is a large 3 plastered in the middle of it.\n[Level 2: Main Hallway] - [Level 2: Card Pick-Up]"

l2_hallway2_desc = "This hallway is very dirty. Dirt, blood, and bones on the floor and wall. There is a creepy painting on the wall of a carnival, with blood smeared into the painting. Also a picture of a random man.\n [Level 2: Main Hallway] - [Level 2: Office] - [Level 2: Surveillance Room]"

l2_surroom_desc = "In this room you find a computer system. Moniters you can hear sounds of a clown. How is this possible? There seems to be no key card in the room. But you do find a big bowling shoe, like that of a clown.\n [Level 2: Hallway 2] - [Level 2: Security Footage]"

l2_cardpickup_info = "[Level 2: Utility Room] - [Level 2: Main Hallway]"

l2_office_desc = "You enter the office to find a child show playing of a clown. There are two windows,one looking out to hallway 2 and one out at the main hallway. At a desk there is a computer emitting sounds that sound like that of a clown.\n[Level 2: Hallway 2] - [Level 2: Computer Screen]"

l2_steelgate_desc = "Enter this gate to go up the stairs to level 3.\n[Level 2: Main Hallway] - [Level 3: Main Hall]"

## LEVEL 3
l3_mh_info = "Welcome to level 3. This floor is very slick and sticky. There is no sign of blood on this floor. There is no other hallways you can enter any location from this location.\n[Level 3: Fence] - [Level 3: Steel Gate] - [Level 3: File and Study Room] - [Level 3: Food Storage] - [Level 3: Washing Station] -[Level 2: Steel Gate]"

l3_ws_desc = "You have walked upon a washing station. You look your self in the mirror and notice how dirty your face is. You wash up.\n[Level 3: Main Hall]"

l3_filestudy_desc = "You have entered the file and study room. This room is a mess, with files scatered and tables turned over. It looks as if someone has scavenged through everything in this room.\n[Level 3: Main Hall]"

l3_fstor_desc = "You have entered what looks like no normal food storage. There is not human food in site. Only food with the label'FOR SCP-999.\n[Level 3: Main Hall]"

l3_fence_desc = "You have opened the gate on the fence and entered. You find the SCP-999. The SCP does not seem harmful. You are safe but you find a GREEN card, there is a large 4 plastered in the middle of it.\n[Level 3: Main Hall] - [Level 3: Orange Slime] - [Level 3: Card Pick-Up]"

l3_orangeslime_desc = "[Level 3: Fence] - [Level 3: Card Pick-Up] - [Level 3: Main Hall]"

l3_sg_desc = "Enter this gate to go up to level 4.\n[Level 4: Lobby] - [Level 3: Main Hall]"

l3_card_desc = "[Level 3: Fence]"

###[                  Level 4                       ]

l4_lobby_info = "You have entered the level 4 lobby. It is a huge space to look around. It looks like a level patients, soldiers, or inmates. \n[Level 4: Library] - [Level 4: Empty Armory] - [Level 4: Hallway 1] - [Level 4: Hallway 2] - [Level 4: Leisure Room] - [Level 4: Food Station] - [Level 4: Steel Gate] - [Level 3: Steel Gate]"

l4_library_desc = "You have entered the library to see that the books that once were readable may no longer be. The books are scathered all over the room, with mold and mossy material growing on them.\n [Level 4: Lobby]"

l4_armory_desc = "You have entered the armory or the remains of one. Their are a few weapons: a gun, an AR, and a bow. unfortunately, there is no ammo.\n[Level 4: Lobby]"

l4_hall1_desc = "In this hallway there is a very horrific smell. *Smells like old remains of something* Go right to enter bunk 2 and left to go to bunk 1.\n[Level 4: Lobby] - [Level 4: Bunk 1] - [Level 4: Bunk 2]"

l4_hall2_desc = "This hallway is very clean and decorated, or was once at least. Go right to enter the lounge and left to enter a bunk.\n[Level 4: Lobby] - [Level 4: Bunk 3]- [Level 4: Lounge]"

l4_leisure_desc = "You have entered the leisure room. This room has a broken tV, which was once used to kill time and relax. A deck of bloody cards and a ping-pong table.\n[Level 4: Lobby]"

l4_fs_desc = "You have entered the food station or what is left of one. You do find one can of chili beans laying in an open cabinet.\n[Level 4: Lobby]"

l4_bunk2_desc = "You have entered a bunk. It has a very bland style. A couple of the bunks or flipped. You search around for a keycard but do not find one. \n[Level 4: Hallway 1]"

l4_bunk1_desc = "As you enter this bunk room. You see a horrific scene. A body hanging from the ceiling. You are freaked out but notice a BLUE card, there is a large 5 plastered in the middle of it. \n[Level 4: Card Pick-Up] - [Level 4: Hallway 1]"

l4_lounge_desc = "You immediately leave the lounge. Locking the door behind you.\n[Level 4: Hallway 2]"

l4_bunk3_desc = "This bunk is divided into two sides of bunks with a table in the middle. The table looks like where friends use to gamble.\n[Level 4: Hallway 2]"

l4_sg_desc = "Enter this gate to go up to level 5.\n[Level 4: Lobby] - [Level 5: Main Hall]"

l4_card_desc = "\n[Level 4: Bunk 1]"

####[                    Level 5                    ]

l5_sg_info = "Enter this gate to go up to Level 6.\n[Level 6] - [Level 5: Main Hall] - [Level 5: Enclosure Hall]"

l5_hall_desc = "Welcome to Level 5:  You see that there are thick windows lining what looks to be a habitat/enclosure.  There is grassy terrain, a pond, a rock, and what looks to be a key card on the far wall.  However, you notice a white-ish humanoid facing the corner, it seems to be cowering,  it looks very emaciated with long unproportionally thin limbs and a large chest.\n[Level 5: Enclosure Hall] - [Level 5: Steel Gate]"

l5_enclosure_desc = "Inside there seems to be gardening tools such as a rake, a shovel, and a hoe.  There's writing on a wall which seems to be a warning and a door that leads to the Habitat of the Grass Terrain.\n[Level 5: Main Hall] - [Level 5: Warning Message] - [Level 5: Grass Terrain] - [Level 5: Steel Gate]"

l5_warnmess_desc = ""

l5_grassterrain_desc = "You are seemingly walking on grass. Suprised by it being well cut because, who could have been to cut it. Their are many elements inside this well kept grass terrain.\n[Level 5: Enclosure Hall] - [Level 5: Tall Grass] - [Level 5: Rock] - [Level 5: Pond] - [Level 5: Card 1 Pick-Up]"

l5_grass_desc = "Tall grass in the middle of a grass terrain. You knowtice a card.\n[Level 5: Card 2: Pick-Up] - [Level 5: Grass Terrain] - [Level 5: Rock] - [Level 5: Pond]"

l5_rock_desc = "A rock in the middle of the grass terrain. The rock is very dirty but shines like some kind of crystal. There is a card next to the rock.\n[Level 5: Card 3 Pick-Up] - [Level 5: Tall Grass] - [Level 5: Grass Terrain] - [Level 5: Pond]"

l5_pond_desc = "A little lake with dead fish floating on top. It is a very dry climate on this level so you wonder how and why their is a pond.\n[Level 5: Card 4 Pick-Up] - [Level 5: Rock] - [Level 5: Tall Grass] - [Level 5: Grass Terrain]"

l5_card1_desc = "\n[Level 5: Grass Terrain]"

l5_card2_desc = "\n[Level 5: Tall Grass]"

l5_card3_desc = "\n[Level 5: Rock]"

l5_card4_desc = "\n[Level 5: Pond]"

####[                     Level 6                      ]

l6_emptyfloor_desc = "Welcome to level 6. Choose Right or Left. Maybe going right is the right decision?* OR it could be reverse psychology* \n[Level 5: Steel Gate] - [Right Staircase] - [Left Staircase]"

rightstaircase = "The entrance of this staircase is identical with the other one..\n[Left Staircase] - [Level 6]"

leftstaircase = "The entrance of this staircase is identical with the other one..\n[Right Staircase] - [Level 6]"


@dataclass
class User:
    name: str
    hp: int  # health
    cl: int  #clearance level
    age: int
    si: str  #special item


def scp_261(destination: str) -> None:
    if destination == "Level 1: Vending Machine":
        while True:
            print("It looks like a normal vending machine..")
            print("Would you like something from it?\n[Yes] or [No]")
            v = input("> ").title()
            if v == "Yes":
                print("What would you like?")
                choice = input("> ").title()
                print(
                    f"The vending machine gives you the liquid form of {choice} in a cup.\n"
                )
                break
            elif v == "No":
                print("You exit the option menu.")
                break
            else:
                print("This is not an option on the machine..")


def scp_993(user: User, destination: str) -> None:
    if destination == "Level 2: Security Footage" or destination == "Level 2: Computer Screen" and user.age > 10:
        print("You have passed out!")
        print("Please wait 30 Seconds to continue")
        x = 30
        while True:
            time.sleep(5)
            x -= 5
            if x < 1:
                print("You May Resume Now.")
                user.hp -= 50
                break
            elif x / 5 > 0:
                print(f"{x} Seconds Remaining...")


def scp_999(user: User, destination: str) -> None:
    if destination == "Level 3: Orange Slime":
        while True:
            print(
                "\nIt's an adorable orange slime... It looks so cute and like it wants to play!"
            )
            print("\n[Play] - [No]")
            x = input("> ").title()
            t = 30
            if x == "Play" and user.hp < 100:
                print(
                    "You decide to play with the orange slime... It bounces and slides around seeming very happy until it notices you in a slight bit of pain.  It slides up to you and wraps around your leg as it emitts a sound like cat's purr, you can feel it through-out your body."
                )
                while True:
                    user.hp = 100
                    time.sleep(2)
                    t -= 5
                    if t < 1:
                        print("You feel so much better now..")
                        break
                    elif t / 5 > 0:
                        print(f"""{t}
It seems to smile at you with it's eyes""")
                break
            elif x == "Play" and user.hp == 100:
                print("You play with the slime and have fun")
                break
            elif x == "No":
                print(
                    "It looks sad, it gives you puppy dog eyes and turns around, defeated.."
                )
                break
            else:
                print("Invalid Input.")


def timed_input(prompt, timeout):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return (sys.stdin.readline().rstrip('\n'))


def scp_173(user: User, destination: str, timed_input) -> None:
    if destination == "Level 4: Lounge":
        x = timed_input(
            "\n\n\n\n\n\n\n                          DANGER                \n\n\n\n\n\n\nYou notice a concrete figure, you have 10 seconds to react.\n[Close Eyes] - [Stare]\n> ",
            timeout)
        if x == "Close Eyes":
            user.hp = 0
            print("You have died\nBilly snapped your neck.")
            quit()
        elif x == "Stare":
            print("You made the right choice.  You're alive.")
        else:
            print(
                "You didn't make a proper decision in time.  You blinked.  Billy snapped your neck."
            )
            user.hp = 0
            quit()


def scp_096(user: User, destination: str) -> None:
    while True:
        print("Do you pick up the card?\n[Yes] or [No]")
        c = input("> ").title()
        if c == "Yes":
            print("Do you check to see if it's the real card?\n[Yes] or [No]")
            cc = input("> ").title()
            if cc == "Yes":
                print(f"""\n\n\n\n\n
                    You check the card and notice the face caught in what seems to be a hollowed scream.
                    \n\n\n\n\n""")
                time.sleep(5)
                print(f"""
                    The blood in your veins nearly turn to Ice as you recognize the creature."""
                      )
                time.sleep(3)
                print(f"""\n\n\n\n\n\n\n
                    !!![The creature in the corner begins to scream]!!!
                    \n\n\n\n\n\n\n""")
                time.sleep(3)
                print(f"""
                    [It stands to it's full height which seems to be well over 7 and half feet tall..]"""
                      )
                time.sleep(4)
                print(f"""
                    [It runs towards you and is infront of you in nearly a blink of an eye.  One of it's arms swings at your face and the world goes black.
                    
                                You have died.]""")
                user.hp = 0
                quit()
            elif cc == "No":
                print("You set the card down.")
                break
            else:
                print("Invalid input.")
        elif c == "No":
            print("You set the card down.")
            break
        else:
            print("Invalid input.")


def scp_087(user: User, destination: str) -> None:
    s = 0
    while True:
        print("Do you enter the staircase?\n[Yes] - [No]")
        x = input("> ").title()
        if x == "Yes":
            s += 1
            print("\nYou start down the descending staircase..")
            if s >= 1:
                print("\nDo you wish to continue down the staircase?\n[Yes] - [No]")
                sc = input("> ").title()
                if sc == "Yes" and s< 3:
                    s += 1
                    print("You continue down the dark staircase..")
                elif sc == "Yes" and s > 2 and s <= 6:
                    s += 1
                    print("You can hear crying.. it sounds distressed.")
                elif sc == "Yes" and s > 6:
                    print(f"""
                    'Why did you keep going..?  Now you have to die..' a voice says between sniffles 'You shouldn't have come down.  Now you're stuck with me...'
                    """)
                    time.sleep(5)
                    print(f"""
                    Forever.
                    """)
                    quit()
                elif sc == "No":
                    s -= 1
                    print("You ascend the staircase.")
        elif x == "No":
            print("You decide not to enter the staircase.")
            break
        else:
            print("This is not a valid option.")


def escape(user: User, destination: str) -> None:
    while True:
        print("Do you enter the staircase?\n[Yes] - [No]")
        x = input("> ").title()
        if x == "Yes":
            print("You have escaped the facility!  Congrats!")
            quit()
        elif x == "No":
            print("You do not enter the staircase.")
            break
        else:
            print("Invalid input.")


def staircase_choice(user: User, destination: str) -> None:
    if destination == "Right Staircase":
        scp_087(user, destination)
    elif destination == "Left Staircase":
        escape(user, destination)


def cl_index() -> None:
    print(cl_desc, c1_desc, c2_desc, c3_desc, c4_desc, c5_desc, c6_desc)


def scp_index():
    print(scp_desc, scp_261_desc, scp_087_desc, scp_173_desc, scp_993_desc,
          scp_096_desc, scp_999_desc)


def card_pickup(user: User) -> None:
    while True:
        print("\nDo you pick up the card?")
        print("[Yes] or [No]")
        cp = input("> ").title()
        if cp == "Yes":
            print("\nYou have picked up the card.")
            if user.cl == 0:
                user.cl = 1
                break
            elif user.cl == 1:
                user.cl = 2
                break
            elif user.cl == 2:
                user.cl = 3
                break
            elif user.cl == 3:
                user.cl = 4
                break
            elif user.cl == 4:
                user.cl = 5
                break
            elif user.cl == 5:
                user.cl = 6
                break
        elif cp == "No":
            print("\nYou chose not to pick up the card.")
            break
        else:
            print("\nThis is not a valid option")


def valid_card_pickup(user: User, destination: str) -> None:
    if destination == "Level 0: Card Pick-Up" and user.cl == 0:
        card_pickup(user)
    elif destination == "Level 1: Card Pick-Up" and user.cl == 1:
        card_pickup(user)
    elif destination == "Level 2: Card Pick-Up" and user.cl == 2:
        card_pickup(user)
    elif destination == "Level 3: Card Pick-Up" and user.cl == 3:
        card_pickup(user)
    elif destination == "Level 4: Card Pick-Up" and user.cl == 4:
        card_pickup(user)
    elif destination == "Level 5: Card 4 Pick-Up" and user.cl == 5:
        card_pickup(user)
    elif destination == "Level 5: Card 1 Pick-Up":
        scp_096(user, destination)
    elif destination == "Level 5: Card 2 Pick-Up":
        scp_096(user, destination)
    elif destination == "Level 5: Card 3 Pick-Up":
        scp_096(user, destination)


def cont_input() -> bool:
    while True:
        print("Do you wish to continue?")
        print("[Yes] or [No]")
        cont = input("> ").title()
        if cont == "Yes":
            return True
        elif cont == "No":
            return False
        else:
            print("This is not a valid input..")


def pickup_item(user: User) -> None:
    while True:
        if user.cl == 1:
            print(
                "You have found a first aid kit it only gives you a 100 more health."
            )
            print("[Yes] or [No]")
            pickup = input("> ").title()
            if pickup == "Yes":
                user.si = "First Aid"
                break
            elif pickup == "No":
                print("You chose not to the the first aid kit up.")
                break


def valid_pickup_item(user: User, destination: str) -> None:
    if destination == "Level 1: Health Pack":
        pickup_item(user)


def use_item(user: User) -> None:
    if user.si == "First Aid":
        user.hp += 100
        user.si = "None"


def user_check(user: User) -> None:
    print(f"""
Name: {user.name}
Health: {user.hp}
Clearance Level: {user.cl}
Age: {user.age}
Item: {user.si}
        """)


def welcome_message() -> None:
    print(welcomemessage)


def ploc_info(location: str) -> None:
    print(f"You are at {location}")
    if location == "Level 0: Hallway":
        print(l0_hallway_info)
    elif location == "Level 0: Card Pick-Up":
        print(l0_cardpickup_info)
    elif location == "Level 0: Steel Gate":
        print(l0_steelgate_info)
    elif location == "Level 1: Hallway 1":
        print(l1_hw1_info)
    elif location == "Level 1: Hallway 2":
        print(l1_hw2_info)
    elif location == "Level 1: Hallway 3":
        print(l1_hw3_info)
    elif location == "Level 1: Hallway 4":
        print(l1_hw4_info)
    elif location == "Level 1: Hallway 5":
        print(l1_hw5_info)
    elif location == "Level 1: Hallway 6":
        print(l1_hw6_info)
    elif location == "Level 1: Hallway 7":
        print(l1_hw7_info)
    elif location == "Level 1: Office":
        print(l1_office_info)
    elif location == "Level 1: Meeting Room":
        print(l1_meetroom_info)
    elif location == "Level 1: Breakroom":
        print(l1_breakroom_info)
    elif location == "Level 1: Health Pack":
        print("YOU HAVE PICKED UP ITEM\n[Level 1: Office]")
    elif location == "Level 1: Supervisor Room":
        print(l1_svroom_info)
    elif location == "Level 1: Card Pick-Up":
        print(l1_cardpickup_info)
    elif location == "Level 1: Steel Gate":
        print(l1_steelgate_info)
    elif location == "Level 1: Vending Machine":
        print(l1_vendingmachine_info)
    elif location == "Level 2: Hall":
        print(l2_hall_info)
    elif location == "Level 2: Main Hallway":
        print(l2_mainhall_desc)
    elif location == "Level 2: Hallway 2":
        print(l2_hallway2_desc)
    elif location == "Level 2: Men's Bathroom":
        print(l2_mb_desc)
    elif location == "Level 2: Women's Bathroom":
        print(l2_wb_desc)
    elif location == "Level 2: Utility Room":
        print(l2_utilroom_desc)
    elif location == "Level 2: Card Pick-Up":
        print(l2_cardpickup_info)
    elif location == "Level 2: Supply Closet":
        print(l2_supplycloset_desc)
    elif location == "Level 2: Office":
        print(l2_office_desc)
    elif location == "Level 2: Surveillance Room":
        print(l2_surroom_desc)
    elif location == "Level 2: Steel Gate":
        print(l2_steelgate_desc)
    elif location == "Level 3: Main Hall":
        print(l3_mh_info)
    elif location == "Level 3: Food Storage":
        print(l3_fstor_desc)
    elif location == "Level 3: Wash Station":
        print(l3_ws_desc)
    elif location == "Level 3: File and Study Room":
        print(l3_filestudy_desc)
    elif location == "Level 3: Fence":
        print(l3_fence_desc)
    elif location == "Level 3: Orange Slime":
        print(l3_orangeslime_desc)
    elif location == "Level 3: Card Pick-Up":
        print(l3_card_desc)
    elif location == "Level 3: Steel Gate":
        print(l3_sg_desc)
    elif location == "Level 4: Lobby":
        print(l4_lobby_info)
    elif location == "Level 4: Hallway 1":
        print(l4_hall1_desc)
    elif location == "Level 4: Hallway 2":
        print(l4_hall2_desc)
    elif location == "Level 4: Empty Armory":
        print(l4_armory_desc)
    elif location == "Level 4: Library":
        print(l4_library_desc)
    elif location == "Level 4: Lounge":
        print(l4_lounge_desc)
    elif location == "Level 4: Leisure Room":
        print(l4_leisure_desc)
    elif location == "Level 4: Food Station":
        print(l4_fs_desc)
    elif location == "Level 4: Bunk 1":
        print(l4_bunk1_desc)
    elif location == "Level 4: Bunk 2":
        print(l4_bunk2_desc)
    elif location == "Level 4: Bunk 3":
        print(l4_bunk3_desc)
    elif location == "Level 4: Card Pick-Up":
        print(l4_card_desc)
    elif location == "Level 4: Steel Gate":
        print(l4_sg_desc)
    elif location == "Level 5: Steel Gate":
        print(l5_sg_info)
    elif location == "Level 5: Main Hall":
        print(l5_hall_desc)
    elif location == "Level 5: Enclosure Hall":
        print(l5_enclosure_desc)
    elif location == "Level 5: Warning Message":
        print(l5_warnmess_desc)
    elif location == "Level 5: Grass":
        print(l5_grass_desc)
    elif location == "Level 5: Pond":
        print(l5_pond_desc)
    elif location == "Level 5: Rock":
        print(l5_rock_desc)
    elif location == "Level 5: Grass Terrain":
        print(l5_grassterrain_desc)
    elif location == "Level 5: Card 1 Pick-Up":
        print(l5_card1_desc)
    elif location == "Level 5: Card 2 Pick-Up":
        print(l5_card2_desc)
    elif location == "Level 5: Card 3 Pick-Up":
        print(l5_card3_desc)
    elif location == "Level 5: Card 4 Pick-Up":
        print(l5_card4_desc)
    elif location == "Level 6":
        print(l6_emptyfloor_desc)
    elif location == "Right Staircase":
        print(rightstaircase)
    elif location == "Left Staircase":
        print(leftstaircase)
    else:
        ...


def valid_location(user: User, location: str, destination: str) -> bool:
    if (user.cl >= 0 and location == "Level 0: Hallway"):
        return destination == "Level 0: Steel Gate" or destination == "Level 0: Card Pick-Up"
    elif location == "Level 0: Card Pick-Up":
        return destination == "Level 0: Hallway" or destination == "Level 0: Steel Gate"
    elif (user.cl >= 1) and location == "Level 0: Steel Gate":
        return destination == "Level 1: Hallway 1" or destination == "Level 0: Hallway" or destination == "Level 0: Card Pick-Up"
    elif location == "Level 0: Steel Gate" and user.cl < 1:
        return destination == "Level 0: Hallway" or destination == "Level 0: Card Pick-Up"

    #Level 1
    elif (location == "Level 1: Hallway 1" and user.cl >= 1):
        return destination == "Level 1: Hallway 7" or destination == "Level 1: Meeting Room" or destination == "Level 1: Hallway 2" or destination == "Level 1: Hallway 3"
    elif location == "Level 1: Meeting Room" and user.cl >= 1:
        return destination == "Level 1: Hallway 1" or destination == "Level 1: Supervisor Room" or destination == "Level 1: Hallway 7"
    elif location == "Level 1: Supervisor Room":
        return destination == "Level 1: Card Pick-Up" or destination == "Level 1: Meeting Room"
    elif location == "Level 1: Card Pick-Up" and user.cl >= 1 and user.cl <= 2:
        return destination == "Level 1: Supervisor Room" or destination == "Level 1: Meeting Room"
    elif location == "Level 1: Hallway 2" and user.cl >= 1:
        return destination == "Level 1: Breakroom" or destination == "Level 1: Hallway 1" or destination == "Level 1: Hallway 4"
    elif location == "Level 1: Hallway 4" and user.cl >= 1:
        return destination == "Level 1: Hallway 6" or destination == "Level 1: Hallway 2" or destination == "Level 1: Hallway 7" or destination == "Level 1: Steel Gate"
    elif location == "Level 1: Breakroom":
        return destination == "Level 1: Hallway 2" or destination == "Level 1: Vending Machine"
    elif location == "Level 1: Vending Machine":
        return destination == "Level 1: Hallway 2" or destination == "Level 1: Breakroom"
    elif location == "Level 1: Hallway 3" and user.cl >= 1:
        return destination == "Level 1: Hallway 1" or destination == "Level 1: Office" or destination == "Level 1: Hallway 5"
    elif location == "Level 1: Hallway 5":
        return destination == "Level 1: Hallway 7" or destination == "Level 1: Hallway 3"
    elif location == "Level 1: Hallway 6":
        return destination == "Level 1: Hallway 4"
    elif location == "Level 1: Supervisor Room":
        return destination == "Level 1: Card Pick-Up" or destination == "Level 1: Meeting Room"
    elif location == "Level 1: Office":
        return destination == "Level 1: Hallway 3" or destination == "Level 1: Health Pack"
    elif location == "Level 1: Health Pack":
        return destination == "Level 1: Office"
    elif location == "Level 1: Hallway 7":
        return destination == "Level 1: Hallway 4" or destination == "Level 1: Hallway 1" or destination == "Level 1: Meeting Room" or destination == "Level 1: Steel Gate"
    elif location == "Level 1: Steel Gate" and user.cl >= 2:
        return destination == "Level 1: Hallway 7" or destination == "Level 2: Hall"
    elif location == "Level 1: Steel Gate" and user.cl < 2:
        return destination == "Level 1: Hallway 7"

    #Level 2
    elif location == "Level 2: Hall":
        return destination == "Level 2: Men's Bathroom" or destination == "Level 2: Women's Bathroom" or destination == "Level 2: Main Hallway" or destination == "Level 1: Steel Gate"
    elif location == "Level 2: Main Hallway":
        return destination == "Level 2: Hallway 2" or destination == "Level 2: Supply Closet" or destination == "Level 2: Utility Room" or destination == "Level 2: Hall" or destination == "Level 2: Steel Gate"
    elif location == "Level 2: Men's Bathroom":
        return destination == "Level 2: Hall"
    elif location == "Level 2: Women's Bathroom":
        return destination == "Level 2: Hall"
    elif location == "Level 2: Supply Closet":
        return destination == "Level 2: Main Hallway"
    elif location == "Level 2: Utility Room":
        return destination == "Level 2: Card Pick-Up" or destination == "Level 2: Main Hallway"
    elif location == "Level 2: Card Pick-Up":
        return destination == "Level 2: Utility Room" or destination == "Level 2: Main Hallway"
    elif location == "Level 2: Hallway 2":
        return destination == "Level 2: Main Hallway" or destination == "Level 2: Office" or destination == "Level 2: Surveillance Room"
    elif location == "Level 2: Surveillance Room":
        return destination == "Level 2: Hallway 2" or destination == "Level 2: Security Footage"
    elif location == "Level 2: Security Footage":
        return destination == "Level 2: Hallway 2"
    elif location == "Level 2: Office":
        return destination == "Level 2: Hallway 2" or destination == "Level 2: Computer Screen"
    elif location == "Level 2: Computer Screen":
        return destination == "Level 2: Office" or destination == "Level 2: Hallway 2"
    elif location == "Level 2: Steel Gate" and user.cl >= 3:
        return destination == "Level 2: Main Hallway" or destination == "Level 3: Main Hall"
    elif location == "Level 2: Steel Gate" and user.cl < 3:
        return destination == "Level 2: Main Hallway"

    #LEVEL 3
    elif location == "Level 3: Main Hall":
        return destination == "Level 3: Wash Station" or destination == "Level 3: File and Study Room" or destination == "Level 3: Food Storage" or destination == "Level 3: Fence" or destination == "Level 3: Steel Gate"
    elif location == "Level 3: Wash Station":
        return destination == "Level 3: Main Hall"
    elif location == "Level 3: Food Storage":
        return destination == "Level 3: Main Hall"
    elif location == "Level 3: File and Study Room":
        return destination == "Level 3: Main Hall"
    elif location == "Level 3: Fence":
        return destination == "Level 3: Main Hall" or destination == "Level 3: Card Pick-Up" or destination == "Level 3: Orange Slime"
    elif location == "Level 3: Orange Slime":
        return destination == "Level 3: Card Pick-Up" or destination == "Level 3: Fence" or destination == "Level 3: Main Hall"
    elif location == "Level 3: Card Pick-Up":
        return destination == "Level 3: Fence" or destination == "Level 3: Orange Slime"
    elif location == "Level 3: Steel Gate" and user.cl >= 4:
        return destination == "Level 3: Main Hall" or destination == "Level 4: Lobby"
    elif location == "Level 3: Steel Gate" and user.cl < 4:
        return destination == "Level 3: Main Hall"

    #LEVEL 4
    elif location == "Level 4: Lobby":
        return destination == "Level 3: Steel Gate" or destination == "Level 4: Steel Gate" or destination == "Level 4: Library" or destination == "Level 4: Empty Armory" or destination == "Level 4: Leisure Room" or destination == "Level 4: Food Station" or destination == "Level 4: Hallway 1" or destination == "Level 4: Hallway 2"
    elif location == "Level 4: Empty Armory":
        return destination == "Level 4: Lobby"
    elif location == "Level 4: Bunk 2":
        return destination == "Level 4: Hallway 1"
    elif location == "Level 4: Bunk 1":
        return destination == "Level 4: Hallway 1" or destination == "Level 4: Card Pick-Up"
    elif location == "Level 4: Card Pick-Up":
        return destination == "Level 4: Bunk 1" or destination == "Level 4: Hallway 1"
    elif location == "Level 4: Food Station":
        return destination == "Level 4: Lobby"
    elif location == "Level 4: Library":
        return destination == "Level 4: Lobby"
    elif location == "Level 4: Lounge":
        return destination == "Level 4: Hallway 2"
    elif location == "Level 4: Leisure Room":
        return destination == "Level 4: Lobby"
    elif location == "Level 4: Hallway 1":
        return destination == "Level 4: Bunk 2" or destination == "Level 4: Bunk 1" or destination == "Level 4: Lobby"
    elif location == "Level 4: Hallway 2":
        return destination == "Level 4: Lounge" or destination == "Level 4: Bunk 3" or destination == "Level 4: Lobby"
    elif location == "Level 4: Bunk 3":
        return destination == "Level 4: Hallway 2"
    elif location == "Level 4: Steel Gate" and user.cl >= 5:
        return destination == "Level 4: Lobby" or destination == "Level 5: Main Hall"
    elif location == "Level 4: Steel gate" and user.cl < 5:
        return destination == "Level 4: Lobby"

    # LEVEL 5
    elif location == "Level 5: Steel Gate" and user.cl >= 6:
        return destination == "Level 5: Main Hall" or destination == "Level 6"
    elif location == "Level 5: Steel Gate" and user.cl < 6:
        return destination == "Level 5: Main Hall"
    elif location == "Level 5: Main Hall":
        return destination == "Level 5: Steel Gate" or destination == "Level 5: Enclosure Hall"
    elif location == "Level 5: Enclosure Hall":
        return destination == "Level 5: Main Hall" or destination == "Level 5: Warning Message" or destination == "Level 5: Grass Terrain"
    elif location == "Level 5: Warning Message":
        return destination == "Level 5: Enclosure Hall" or destination == "Level 5: Grass Terrain"
    elif location == "Level 5: Grass Terrain":
        return destination == "Level 5: Rock" or destination == "Level 5: Pond" or destination == "Level 5: Tall Grass" or destination == "Level 5: Card 1 Pick-Up" or destination == "Level 5: Enclosure Hall"
    elif location == "Level 5: Card 1 Pick-Up":
        return destination == "Level 5: Grass Terrain"
    elif location == "Level 5: Pond":
        return destination == "Level 5: Grass Terrain" or destination == "Level 5: Tall Grass" or destination == "Level 5: Rock" or destination == "Level 5: Card 4 Pick-Up"
    elif location == "Level 5: Card 4 Pick-Up":
        return destination == "Level 5: Pond"
    elif location == "Level 5: Rock":
        return destination == "Level 5: Grass Terrain" or destination == "Level 5: Pond" or destination == "Level 5: Tall Grass" or destination == "Level 5: Card 3 Pick-Up" or destination == "Level 5: Enclosure Hall"
    elif location == "Level 5: Card 2 Pick-Up":
        return destination == "Level 5: Tall Grass"
    elif location == "Level 5: Tall Grass":
        return destination == "Level 5: Card 2 Pick-Up" or destination == "Level 5: Grass Terrain" or destination == "Level 5: Rock" or destination == "Level 5: Pond"
    elif location == "Level 5: Card 3 Pick-Up":
        return destination == "Level 5: Rock"

    ###LEVEL 6
    elif location == "Level 6":
        return destination == "Level 5: Steel Gate" or destination == "Right Staircase" or destination == "Left Staircase"
    elif location == "Right Staircase":
        return destination == "Left Staircase" or destination == "Level 6"
    elif location == "Left Staircase":
        return destination == "Right Staircase" or destination == "Level 6"
    else:
        return False


def enemy_attack(location) -> None:
    if location == "Level 1: Breakroom":
        print(
            "You realize the vending machine is SCP. Do you[Run] or [Go towards]"
        )
        action = input("> ")
        if action == "Run":
            print("You have escaped the SCP!")
        elif action == "Go towards":
            quit()
        else:
            ("You only have two options")


def is_number() -> int:
    while True:
        age = input("Enter Age: ")
        if age.isdigit():
            return int(age)
        else:
            print("This is not a valid input")


def print_user_info(user: User) -> None:
    if user.age <= 110 and user.age >= 7:
        print(f"""
Name: {user.name}
Health: {user.hp}
Clearance Level: {user.cl}
Age: {user.age}
Item: {user.si}
        """)
    elif user.age < 7:
        print("You are to young!!!")
        quit()

    else:
        print("You should be dead!!!")
        quit()


def dest_inp(user: User, location: str) -> str:
    while True:
        print(f"\nYou are currently in {location}\n")
        print("Where would you like to go?")
        destination = input("> " ).title()
        if destination == "Q" or destination == "Check" or destination == "Use Item" or valid_location(
                user, location, destination):
            return destination
        else:
            print(
                "This is an invalid transition! If you are at a Steel Gate you may not have the correct Clearance Level!"
            )


def main() -> None:
    cl_index()
    scp_index()
    print("!!!You can enter [Check] to check your status!!!")
    cont = cont_input()
    if cont:
        welcome_message()
        user = User(input("What is your name? "), 100, 0, is_number(), "None")
        print_user_info(user)
        location = startlocation
        while True:
            ploc_info(location)
            destination = dest_inp(user, location)
            valid_card_pickup(user, destination)
            valid_pickup_item(user, destination)
            scp_261(destination)
            scp_993(user, destination)
            scp_999(user, destination)
            scp_173(user, destination, timed_input)
            staircase_choice(user, destination)
            if destination == "Q":
                break
            elif destination == "Check":
                user_check(user)
            elif destination == "Use Item":
                use_item(user)
            else:
                location = destination
    else:
        print("You escorted yourself off the premises.")


if __name__ == '__main__':
    main()
