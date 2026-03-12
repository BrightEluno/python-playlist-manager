class Song:
    def __init__(self, name: str, singer: str, genre: str):

        self.name = name
        self.singer = singer
        self.genre = genre


    def update(self, name: str = None, singer: str = None, genre: str = None):
        if name is not None:
            self.name = name
        if singer is not None:
            self.singer = singer
        if genre is not None:
            self.genre =genre

    def key(self) -> tuple:
        return (self.name.strip().lower(), self.singer.strip().lower())
    
    
    def __str__(self) -> str:
        return f"{self.name } by {self.singer} ({ self.genre})"

        


        