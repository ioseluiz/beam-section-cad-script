from pyautocad import Autocad, APoint

class Drawing():
    def __init__(self, width, height, rebar_data, stirrup):
        self.width = width
        self.height = height
        self.rebar_data = rebar_data # list of dictionaries with rebar info
        self.stirrup = stirrup
        #self.concrete = concrete
        # Get rectangle coordinates
        self.rect_coordinates = self.get_rect_coordinates()
        print(self.rect_coordinates)
        # Append diameter to rebar_data
        self.append_rebar_diameter()
        print(self.rebar_data)

        # Start ACAD drawing
        self.create_drawing()

    def get_rect_coordinates(self):
        coordinates = []
        # First Point
        coordinates.append(
            {
                'point_id': 1,
                'coor_x': 0,
                'coor_y': 0
            }
        )
        # Second Point
        coordinates.append(
            {
                'point_id': 2,
                'coor_x': 0,
                'coor_y': self.height
            }
        )

        # Third Point
        coordinates.append(
            {
                'point_id': 3,
                'coor_x': self.width,
                'coor_y': self.height,
            }
        )

        # Fourth Point
        coordinates.append(
            {
                'point_id': 4,
                'coor_x': self.width,
                'coor_y': 0
            }
        )

        return coordinates 


    def get_rebar_diameter(self, bar_id):
        # Units in mm
        print(bar_id)
        rebar_info = [
            {
                'id': '#3',
                'diameter': 9.525,
            },
            {
                'id': '#4',
                'diameter': 12.7,
            },
            {
                'id': '#5',
                'diameter': 15.875,
            },
            {
                'id': '#6',
                'diameter': 19.05,
            },
            {
                'id': '#7',
                'diameter': 22.225,
            },
            {
                'id': '#8',
                'diameter': 25.4,
            }
            ]
        
        rebar_diameter = [rebar for rebar in rebar_info if rebar['id'] == bar_id]
        return rebar_diameter[0]['diameter']

    def append_rebar_diameter(self):
        for index in range(0, len(self.rebar_data)):
            self.rebar_data[index]['diameter'] = self.get_rebar_diameter(self.rebar_data[index]['rebar_id'])

    def append_rebar_cad_point(self):
        for index in range(0, len(self.rebar_data)):
            self.rebar_data[index]['cad_point'] = APoint(self.rebar_data[index]['coor_x'], self.rebar_data[index]['coor_y'])

    def draw_rebars(self):
        cad_rebars = []
        for index in range(0, len(self.rebar_data)):
            cad_rebars.append(self.acad.model.addCircle(self.rebar_data[index]['cad_point'], self.rebar_data[index]['diameter']/2))
        for bar in cad_rebars:
            bar.layer = 'Rebar'
            bar.color = 5 # Blue

    def get_max_min_rebar_coordinates(self):

        values = {
                'min_x': self.rebar_data[0]['coor_x'] - self.rebar_data[0]['diameter']/2,   
                'min_x_id': self.rebar_data[0]['id'],
                'max_x': self.rebar_data[0]['coor_x'] + self.rebar_data[0]['diameter']/2,
                'max_x_id': self.rebar_data[0]['id'],
                'min_y': self.rebar_data[0]['coor_y'] - self.rebar_data[0]['diameter']/2,
                'min_y_id': self.rebar_data[0]['id'],
                'max_y': self.rebar_data[0]['coor_y'] + self.rebar_data[0]['diameter']/2,
                'max_y_id': self.rebar_data[0]['id'],
            }
        for index in range(0, len(self.rebar_data)):

            eval_coor = {
                'coor_left': self.rebar_data[index]['coor_x'] - self.rebar_data[index]['diameter']/2,
                'coor_right': self.rebar_data[index]['coor_x'] + self.rebar_data[index]['diameter']/2,
                'coor_bottom': self.rebar_data[index]['coor_y'] - self.rebar_data[index]['diameter']/2,
                'coor_top': self.rebar_data[index]['coor_y'] + self.rebar_data[index]['diameter']/2,
            }
            # Compare with actual values
            if eval_coor['coor_left'] < values['min_x']:
                values['min_x'] = eval_coor['coor_left']
                values['min_x_id'] = self.rebar_data[index]['id']

            if eval_coor['coor_right'] > values['max_x']:
                values['max_x'] = eval_coor['coor_right']
                values['max_x_id'] = self.rebar_data[index]['id']

            if eval_coor['coor_bottom'] < values['min_y']:
                values['min_y'] = eval_coor['coor_bottom']
                values['min_y_id'] = self.rebar_data[index]['id']

            
            if eval_coor['coor_top'] > values['max_y']:
                values['max_y'] = eval_coor['coor_top']
                values['max_y_id'] = self.rebar_data[index]['id']

        return values

    def get_rebar_diameter_by_id(self, bar_id):
        rebar_diameter = [rebar for rebar in self.rebar_data if rebar['id'] == bar_id]
        return rebar_diameter[0]['diameter']


    def get_inner_stirrups_coordinates(self):
        coordinates = []
        outer_rebar_coordinates = self.get_max_min_rebar_coordinates()
        print(outer_rebar_coordinates)
        print(self.get_rebar_diameter_by_id(outer_rebar_coordinates['min_x_id']))
        # Point 1
        coordinates.append(APoint(outer_rebar_coordinates['min_x'], outer_rebar_coordinates['min_y'] + self.get_rebar_diameter_by_id(outer_rebar_coordinates['min_x_id'])/2 ))
        # Point 2
        coordinates.append(APoint(outer_rebar_coordinates['min_x'], outer_rebar_coordinates['max_y'] - self.get_rebar_diameter_by_id(outer_rebar_coordinates['max_y_id'])/2 ))
        # Point 3
        coordinates.append(APoint(outer_rebar_coordinates['min_x'] + self.get_rebar_diameter_by_id(outer_rebar_coordinates['min_x_id'])/2, outer_rebar_coordinates['max_y'] ))
        # Point 4
        coordinates.append(APoint(outer_rebar_coordinates['max_x'] - self.get_rebar_diameter_by_id(outer_rebar_coordinates['max_x_id'])/2, outer_rebar_coordinates['max_y']))
        # Point 5
        coordinates.append(APoint(outer_rebar_coordinates['max_x'], outer_rebar_coordinates['max_y'] - self.get_rebar_diameter_by_id(outer_rebar_coordinates['max_y_id'])/2))
        # Point 6
        coordinates.append(APoint(outer_rebar_coordinates['max_x'], outer_rebar_coordinates['min_y'] + self.get_rebar_diameter_by_id(outer_rebar_coordinates['min_y_id'])/2))
        # Point 7
        coordinates.append(APoint(outer_rebar_coordinates['max_x'] - self.get_rebar_diameter_by_id(outer_rebar_coordinates['max_x_id'])/2, outer_rebar_coordinates['min_y']))
        # Point 8
        coordinates.append(APoint(outer_rebar_coordinates['min_x'] + self.get_rebar_diameter_by_id(outer_rebar_coordinates['min_x_id'])/2, outer_rebar_coordinates['min_y']))

        return coordinates

    def get_outer_strirrups_coordinates(self, bar_diameter):
        coordinates = []
        outer_rebar_coordinates = self.get_max_min_rebar_coordinates()

         # Point 1
        coordinates.append(APoint(outer_rebar_coordinates['min_x'] - bar_diameter, outer_rebar_coordinates['min_y'] + self.get_rebar_diameter_by_id(outer_rebar_coordinates['min_x_id'])/2 ))
        # Point 2
        coordinates.append(APoint(outer_rebar_coordinates['min_x'] - bar_diameter, outer_rebar_coordinates['max_y'] - self.get_rebar_diameter_by_id(outer_rebar_coordinates['max_y_id'])/2 ))
        # Point 3
        coordinates.append(APoint(outer_rebar_coordinates['min_x'] + self.get_rebar_diameter_by_id(outer_rebar_coordinates['min_x_id'])/2, outer_rebar_coordinates['max_y'] + bar_diameter ))
        # Point 4
        coordinates.append(APoint(outer_rebar_coordinates['max_x'] - self.get_rebar_diameter_by_id(outer_rebar_coordinates['max_x_id'])/2, outer_rebar_coordinates['max_y'] + bar_diameter))
        # Point 5
        coordinates.append(APoint(outer_rebar_coordinates['max_x'] + bar_diameter, outer_rebar_coordinates['max_y'] - self.get_rebar_diameter_by_id(outer_rebar_coordinates['max_y_id'])/2))
        # Point 6
        coordinates.append(APoint(outer_rebar_coordinates['max_x'] + bar_diameter, outer_rebar_coordinates['min_y'] + self.get_rebar_diameter_by_id(outer_rebar_coordinates['min_y_id'])/2))
        # Point 7
        coordinates.append(APoint(outer_rebar_coordinates['max_x'] - self.get_rebar_diameter_by_id(outer_rebar_coordinates['max_x_id'])/2, outer_rebar_coordinates['min_y'] - bar_diameter))
        # Point 8
        coordinates.append(APoint(outer_rebar_coordinates['min_x'] + self.get_rebar_diameter_by_id(outer_rebar_coordinates['min_x_id'])/2, outer_rebar_coordinates['min_y'] - bar_diameter))

        return coordinates






    def create_drawing(self):
        self.acad = Autocad(create_if_not_exists=True)

        # Access AcadApplication object
        acad_object = self.acad.ActiveDocument.DimStyles
        print(acad_object)
        

        # Add layers to document
        self.acad.ActiveDocument.Layers.add('Rebar')
        self.acad.ActiveDocument.Layers.add('Concrete')
        self.acad.ActiveDocument.Layers.add('Text')
        self.acad.ActiveDocument.Layers.add('Dimensions')

        # Add DimStyles
        print(self.acad.ActiveDocument.GetVariable("DIMSCALE"))
        print(self.acad.ActiveDocument.GetVariable("DIMBLK"))
        estilo1 = self.acad.ActiveDocument.DimStyles.add('Acotaciones')
        for item in self.acad.ActiveDocument.DimStyles:
            print(vars(item))

        
        # Draw concrete beam
        cover = 50
        # stirrup diameter
        stirrup_diameter = self.get_rebar_diameter(self.stirrup)
        print(stirrup_diameter)
        # Points
        rect_points = []
        print(type(self.rect_coordinates))

        
        for punto in self.rect_coordinates:
            rect_points.append(APoint(punto['coor_x'], punto['coor_y']))

        # Draw rectangle lines
        line1 = self.acad.model.AddLine(rect_points[0], rect_points[1])
        line1.layer = 'Concrete'
        line1.color = 3 # Green
        line2 = self.acad.model.AddLine(rect_points[1], rect_points[2])
        line2.layer = 'Concrete'
        line2.color = 3 # Green
        line3 = self.acad.model.AddLine(rect_points[2], rect_points[3])
        line3.layer = 'Concrete'
        line3.color = 3 # Green
        line4 = self.acad.model.AddLine(rect_points[3], rect_points[0])
        line4.layer = 'Concrete'
        line4.color = 3 # Green

        # Append rebar cad points to rebar_data
        self.append_rebar_cad_point()

        # Draw rebars based on coordinates provided
        self.draw_rebars()

        # Draw stirrups - outer ring
        
        
        # Draw inner lines
        inner_stirrups_coordinates = self.get_inner_stirrups_coordinates()
        line5 = self.acad.model.AddLine(inner_stirrups_coordinates[0], inner_stirrups_coordinates[1])
        line5.layer = 'Rebar'
        line5.color = 5
        line6 = self.acad.model.AddLine(inner_stirrups_coordinates[2], inner_stirrups_coordinates[3])
        line6.layer = 'Rebar'
        line6.color = 5
        line7 = self.acad.model.AddLine(inner_stirrups_coordinates[4], inner_stirrups_coordinates[5])
        line7.layer = 'Rebar'
        line7.color = 5
        line8 = self.acad.model.AddLine(inner_stirrups_coordinates[6], inner_stirrups_coordinates[7])
        line8.layer = 'Rebar'
        line8.color = 5

        # Draw outer lines
        outer_stirrups_coordinates = self.get_outer_strirrups_coordinates(stirrup_diameter)
        line9 = self.acad.model.AddLine(outer_stirrups_coordinates[0], outer_stirrups_coordinates[1])
        line9.layer = 'Rebar'
        line9.color = 5
        line10 = self.acad.model.AddLine(outer_stirrups_coordinates[2], outer_stirrups_coordinates[3])
        line10.layer = 'Rebar'
        line10.color = 5
        line11 = self.acad.model.AddLine(outer_stirrups_coordinates[4], outer_stirrups_coordinates[5])
        line11.layer = 'Rebar'
        line11.color = 5
        line12 = self.acad.model.AddLine(outer_stirrups_coordinates[6], outer_stirrups_coordinates[7])
        line12.layer = 'Rebar'
        line12.color = 5

        # Draw 4 arcs to close stirrup ringS

        # Draw ring hook


        # Drawing title (scale 1:10)
        title_text = self.acad.model.AddText("DETALLE C-X", APoint(0, -150), 50)
        title_text.layer = 'Text'
        scale_text = self.acad.model.AddText("ESCALA 1:10", APoint(0, -200), 30)
        scale_text.layer = 'Text'

        # Draw dimensions
        start_width = APoint(0,0)
        end_width = APoint(self.width, 0)
        position_dim_width = APoint(self.width/2, -50)
        width_dimension = self.acad.model.AddDimAligned(start_width, end_width, position_dim_width)
        width_dimension.layer = 'Dimensions'







        




       



            












