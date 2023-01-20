import hashlib, os, base64, random, time

class SessionManager:
    def __init__(self, secret:str="", max_session_age:int|None=60*60*24*30, hashlen:int|None=16):
        """
        Generate sessions with hashing.

        :secret:                "private key", used to "sign" sessions
        :max_session_age:       time in seconds for session to be expired (default is 1 month)
        :hashlen:               length of "signature" in bytes (to brute force: 8 -> 2w, 9 -> 10y)

        eg:

        sm = SessionManager(secret=os.urandom(16).hex())
        session = sm.generate_session_token("My user's id")
        print(f"Generated session: {session}")
        print(f"Recovered Data: {sm.read_session_token(session)}")
        invalid_session = session[:-1] + "a"
        try:
            sm.read_session_token(invalid_session)
            print("Invalid session was valid?")
        except ValueError as e:
            print(f"Error trying to read invalid session: {e}")

        """
        self.secret = secret
        self.max_session_age =  max_session_age
        self.hashlen = hashlen

    def random_string(self, n=8):
        return ''.join(random.choice("1234567890abcdefghijklmnopqrstuvwxyz") for _ in range(n))

    def generate_session_token(self, user_id=None):
        """
        Take a user_id and return generated session.
        """
        if user_id is None: user_id = self.random_string()

        session = user_id
        if self.max_session_age:
            session += f"-{int(time.time()) + self.max_session_age}"
        
        session = session.encode()
        hashed = hashlib.sha256(session + self.secret.encode())
        
        if self.hashlen:
            hashed = hashed.digest()[:self.hashlen]

        return base64.urlsafe_b64encode(session + hashed).decode()
    
    def read_session_token(self, session):
        """
        Take a generated session and return user_id, raise error if invalid. 
        """
        session = base64.urlsafe_b64decode(session)
        session, signature = session[:-self.hashlen], session[-self.hashlen:]
        
        session_hash = hashlib.sha256(session + self.secret.encode()).digest()
        if self.hashlen:
            session_hash = session_hash[:self.hashlen]
        
        if signature != session_hash:
            raise ValueError("Invalid session token")
        
        session = session.decode()
        if self.max_session_age:
            timestamp = session.split("-")[-1]
            if time.time() > float(timestamp):
                raise ValueError("Session expired")
        
        user_id = "-".join(session.split("-")[:-1])

        return user_id
    
if __name__ == "__main__":
    sm = SessionManager(secret=os.urandom(16).hex())
    session = sm.generate_session_token("My user's id")
    print(f"Generated session: {session}")
    print(f"Recovered Data: {sm.read_session_token(session)}")
    invalid_session = session[:-1] + "a"
    try:
        sm.read_session_token(invalid_session)
        print("Invalid session was valid?")
    except ValueError as e:
        print(f"Error trying to read invalid session: {e}")
