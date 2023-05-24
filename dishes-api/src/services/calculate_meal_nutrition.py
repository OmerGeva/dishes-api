class CalculateMealNutrition():
    def __init__(self,  col, attrs):
        self.col = col
        self.attrs = attrs
        
    def call(self):
        dish_ids = [self.attrs['appetizer'], self.attrs['main'], self.attrs['dessert']]
        self.attrs['cal'] = self.attrs['sodium'] = self.attrs['sugar'] = 0
        
        for id in dish_ids:
            if not id:
                continue

            dish = self.col.dishes.get(id)

            if not dish:
                return []
            
            self.attrs['cal'] += dish['cal']
            self.attrs['sodium'] += dish['sodium']
            self.attrs['sugar'] += dish['sugar']
        
        return self.attrs