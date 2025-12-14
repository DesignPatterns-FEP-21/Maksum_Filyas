class StudentGroup:
    def __init__(self, name: str):
        self.name = name
        self.sessions = []

    def add_session(self, session):
        for s in self.sessions:
            if s.time == session.time:
                raise ValueError(f"Конфлікт занять: {session} співпадає з {s}")
        self.sessions.append(session)

    def check_conflicts(self):
        conflicts = []
        seen = {}
        for s in self.sessions:
            if s.time in seen:
                conflicts.append((seen[s.time], s))
            else:
                seen[s.time] = s
        return conflicts