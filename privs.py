# Privliges. yay...
# bitwise enumeration for lists of privliges in ripple, essentially for the creation of permission groups


from enum import IntFlag # thing for class
import json # for putting in permissions.json.
import pick

# the class for privliges
class Privileges(IntFlag):
    NoPrivs             = 0        # the user has no privliges, aka. banned
    PublicUser          = 1        # the user is visible in user search on website
    NormalUser          = 2 << 0   # the user has a profile and has logged in atleast once
    Donor               = 2 << 1   # the user is a donor
    AccessRAP           = 2 << 2   # can accdess kap
    ManageUsers         = 2 << 3   # can edit users in kap
    BanUsers            = 2 << 4   # wow i wonder what this does
    SilenceUsers        = 2 << 5   # can silence users
    WipeUsers           = 2 << 6   # can wipe users
    ManageBeatmaps      = 2 << 7   # BN stuff, ranking loving, etc.
    ManageServers       = 2 << 8   # can manage servers in kap.
    ManageSettings      = 2 << 9   # server settings in kap.
    ManageBetaKeys      = 2 << 10  # what the name is. i have no clue how it works.
    ManageReports       = 2 << 11  # reports in kap.. apparently.
    ManageDocs          = 2 << 12  # can manage docs? idk?
    ManageBadges        = 2 << 13  # can manage badges in kap.
    ViewRAPLog          = 2 << 14  # can view logs in kap.
    ManagePrivs         = 2 << 15  # can change privliges of users
    SendAlerts          = 2 << 16  # those annoyinh badge notifications in the bottom right
    ChatMod             = 2 << 17  # this permission is confusing, everything else is covered? i guess just for GMT?
    KickUsers           = 2 << 18  # can kick users from the server, from in-game commands.
    PendingVerify       = 2 << 19  # users who haven't signed in
    TournamentStaff     = 2 << 20  # tournament stuff? no clue how it works but for tournaments
    Caker               = 2 << 21  # absolutely no clue
    ManageClans         = 2 << 27  # can manage clans in kap.
    ViewIps             = 2 << 28  # can view ips in kap.
    IsBot               = 2 << 30  # the user is a bot. wow. prevents like.. being banned and stuff
    ViewTopScores       = 2 << 31 
    PanelNominate       = 2 << 32
    PanelNominateAccept = 2 << 33
    PanelOverwatch      = 2 << 34
    PanelErrorLogs      = 2 << 35

# Bitwise enumerations are powers of 2, so they're expressed in binary.
# when we combine them, we can use this to decipher if a user has privliges, from just one number, which, is easy(er) then a giant list.

# this is a undertaking i was not willing to do. several days will be spent on this

# for further refrence, we add a privlige to a int type var by;
# var |= Privileges.priv
# and to see if a privlige is in a var, we do;
# var & Privileges.priv
    
def getprivfromint(privint):
    # Get a list of privs from an integer
    privs = [priv.name for priv in Privileges if privint & priv]
    if len(privs) == 0:
        raise ValueError("No Privileges")
    return privs

def getintfrompriv(privs):
    # Get an integer from a list of privs
    privint = 0
    # Convert the list of privs to a list of Privileges
    privs = [Privileges[priv] for priv in privs]
    for priv in privs:
        privint |= priv.value
    return privint

def setprivgroups(): # only for creating groups in permissions.json
    # get permissions.json
    with open("permissions.json", "r") as jsonfile:
        permissions = json.load(jsonfile)
    # make groups into list
    permissions = list(permissions.keys())
    for group in permissions:
        # use pick to have user select privs
        title = f'Select permissions for {group}'
        options = [priv.name for priv in Privileges]
        selected = pick.pick(options, title, multiselect=True, min_selection_count=1)
        # parse tuple to list
        selected = [priv[0] for priv in selected]
        # get int from privs
        privint = getintfrompriv(selected)
        # open json with write perms
        with open("permissions.json", "r") as f:
            perm = json.load(f)
            perm[group]["Value"] = privint
            perm[group]["Permissions"] = selected
        # replace json
        with open("permissions.json", "w") as f:
            json.dump(perm, f, indent=4)

def createQuery(): # only for creating query for pushing json to db
    # create a query for pushing json to db
    with open("permissions.json", "r") as f:
        j = json.load(f)
        # delete everything from privileges_groups_new
        query = "DELETE FROM privileges_groups_new;\n"
        for group in j.keys():
            query += "INSERT INTO privileges_groups_new (name, privileges, color) VALUES ('{}', {}, 'default');\n".format(group, str(j[group]["Value"]))
        
        print(query)



  