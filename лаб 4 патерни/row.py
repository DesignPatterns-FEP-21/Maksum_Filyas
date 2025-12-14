# зберігає один рядок таблиці —  набір даних у вигляді словника {назва_колонки: значення} — і має унікальний ідентифікатор id для кожного рядка.
class Row:
    def __init__(self, data=None):
        self.id = None
        self.data = data or {}
    
    def __getitem__(self, key):
        return self.data.get(key)
    
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def keys(self):
        return self.data.keys()
    
    def get(self, key, default=None):
        return self.data.get(key, default)