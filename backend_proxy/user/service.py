from backend_proxy.db.mongoDB import MongoDB
from backend_proxy.user.schema import UserSchema
import backend_proxy.misc.util as util
import datetime as dt
import requests
import bcrypt


class UserService:

    def __init__(self):
        self.db = MongoDB("user")

    def login_user(self, req_dict):
        user = self.db.find({"username": req_dict["username"]})
        if user is None:
            raise Exception(
                "User {} does not exist".format(req_dict["username"]))
        if bcrypt.checkpw(req_dict["password"].encode('utf-8'), user["password"]):
            user["last_seen_at"] = dt.datetime.now()
            self.db.update({"username": user["username"]}, user)
            return user
        else:
            raise Exception("Password is incorrect...")

    def register_user(self, req_dict, session):
        # token is needed since registration can be done only by admins
        self.assert_logged_in(session)
        session_user = self.db.find({"username": session["username"]})
        if session_user is None or "admin" not in session_user["roles"]:
            raise Exception("You have no right to register a user.")
        password = req_dict["password1"]
        if password != req_dict["password2"]:
            raise Exception("Password don't match.")
        pass_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = {k: req_dict[k]
                for k in ["username", "email", "roles", "tools"]}
        user["password"] = pass_hashed
        user["last_seen_at"] = dt.datetime.now()
        user["registered_at"] = user["last_seen_at"]
        self.db.create(user)
        return self.dump(user)

    def update_user(self, req_dict, session):
        # either the admin or the user-itself
        self.assert_logged_in(session)
        username = session["username"]
        session_user = self.db.find({"username": username})
        if "admin" in session_user["roles"]:
            original_username = req_dict["original_username"]
            target_user = self.db.find({"username": original_username})
            target_keys = ["email", "username", "roles", "tools"]
        else:
            target_user = session_user
            target_keys = ["email", "username"]
            original_username = target_user["username"]
        if (original_username != req_dict["new_username"] and
                self.db.find({"username": req_dict["new_username"]})):
            raise Exception("Username: {} already taken"
                            .format(req_dict["new_username"]))

        username = req_dict["new_username"]
        password = req_dict["new_password1"]
        if password != req_dict["new_password2"]:
            raise Exception("Password don't match.")
        pass_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        for key in target_keys:
            target_user[key] = req_dict[key]
        target_user["password"] = pass_hashed
        target_user["last_seen_at"] = dt.datetime.now()
        self.db.update({"username": original_username}, target_user)
        return self.dump(target_user)

    def add_tool_to_user(self, session, tool_enum):
        self.assert_logged_in(session)
        username = session["username"]
        session_user = self.db.find({"username": username})
        session_user["tools"].append(tool_enum)
        self.db.update({"username": username}, session_user)
        return self.dump(session_user)

    def get_current_user(self, session):
        self.assert_logged_in(session)
        session_user = self.db.find({"username": session["username"]})
        self.dump(session_user)

    def get_users(self, session):
        self.assert_logged_in(session)
        session_user = self.db.find({"username": session["username"]})
        if "admin" not in session_user["roles"]:
            raise Exception("You don't have the right to see other users")
        tools = self.db.find_all()
        return [self.dump(tool) for tool in tools]

    def get_tools_user(self, session):
        self.assert_logged_in(session)
        session_user = self.db.find({"username": session["username"]})
        if "admin" in session_user["roles"]:
            # None is special placeholder for all tools
            return None
        else:
            tools = session_user["tools"]
            tools = [] if tools is None else tools
            return tools

    def assert_logged_in(self, session):
        if "username" not in session:
            raise("You are not logged in.")

    def dump(self, obj):
        return UserSchema(exclude=['_id', 'password']).dump(obj)
