from bson import ObjectId


class CalculateMealNutrition():
    def __init__(self,  col, attrs):
        self.col = col
        self.attrs = attrs
        
    def call(self):
        dishIDs = [self.attrs['appetizer'], self.attrs['main'], self.attrs['dessert']]
        self.attrs['cal'] = self.attrs['sodium'] = self.attrs['sugar'] = 0
        
        for id in dishIDs:
            if not id:
                continue

            dish = self.col.find_data_item(self.col.dishes, 'ID', id)

            if dish == -1:
                return []
            
            self.attrs['cal'] += dish['cal']
            self.attrs['sodium'] += dish['sodium']
            self.attrs['sugar'] += dish['sugar']
        
        return self.attrs