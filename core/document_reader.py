import re
from enum import Enum
import openpyxl
from core.data_model import InputData
import core.data_model as dm
import datetime as dt


class DocumentReader():
    class DirectionOfGroupingUp(Enum):
        TOP = 0
        BOTTOM = 1
        RIGHT = 2
        LEFT = 3

    def getMergedCellVal(self, sheet, cell):
        rng = [s for s in sheet.merged_cells.ranges if cell.coordinate in s]
        return sheet.cell(rng[0].min_row, rng[0].min_col).value if len(rng)!=0 else cell.value
    
    def unMergeCells(self, sheet_obj, processed):
        for i_row in range(1,self.data.rowMax):
            for i_col in range(1, self.data.colMax):              
                cell = sheet_obj.cell(row=i_row, column=i_col)
                if isinstance(cell, openpyxl.cell.cell.MergedCell):
                    value_merged = self.getMergedCellVal(sheet_obj, cell)
                    processed[i_row][i_col] = value_merged             
                else:
                    processed[i_row][i_col] = sheet_obj.cell(row =  i_row, column = i_col).value
    
    def detectClass(self, string):
        if "пара" in string:
            return True
        else:
            return False
 
    def detectTime(self, string):
        res = re.search("[+-]?([0-9]*[.])?[0-9]+?\/[+-]?([0-9]*[.])?[0-9]+", string)
        if res:
            return True
        else:
            return False
    
    def detectPartOfGroup(self, string):
        if "п/гр" in string:
            return True
        else:
            return False    
    
    def groupUpBorders(self, sheet_obj, processed, direction : DirectionOfGroupingUp):
        def check(i_row_parent, i_col_parent, i_row, i_col, is_going, sheet_obj, processed, direction : self.DirectionOfGroupingUp):
            def checkAny(cell):
                if cell.border.top.style != None or \
                    cell.border.bottom.style != None or \
                    cell.border.left.style != None or \
                    cell.border.right.style != None:
                    return True
                else:
                    return False
            def checkAll(cell):
                if cell.border.top.style != None and \
                    cell.border.bottom.style != None and \
                    cell.border.left.style != None and \
                    cell.border.right.style != None:
                    return True
                else:
                    return False
            def checkSide(cell, direction : self.DirectionOfGroupingUp):
                def checkTop(cell):
                    if cell.border.top.style == None:
                        return True
                    else:
                        return False
                def checkBottom(cell):
                    if cell.border.bottom.style == None:
                        return True
                    else:
                        return False
                if direction == self.DirectionOfGroupingUp.TOP:
                    return checkTop(cell)
                elif direction == self.DirectionOfGroupingUp.BOTTOM:
                    return checkBottom(cell)
            
            cell = sheet_obj.cell(row=i_row, column=i_col)
            origin_cell = sheet_obj.cell(row=i_row_parent, column=i_col_parent)
            if checkAny(cell):
                if checkAll(cell) == False:
                    if cell.value != None:
                        if not self.detectClass(cell.value):
                            if checkSide(cell, direction):
                                if self.detectTime(cell.value) == False:
                                    if self.detectPartOfGroup(cell.value) == False:
                                        if i_row < self.data.rowMax and  i_col < self.data.colMax:                                                
                                            if direction == self.DirectionOfGroupingUp.TOP:
                                                if (i_row - 1) > 1:
                                                    processed[i_row - 1][i_col] = origin_cell.value
                                                    is_going = True
                                                    check(i_row_parent, i_col_parent, i_row - 1, i_col, is_going, sheet_obj, processed, direction)
                                            if direction == self.DirectionOfGroupingUp.BOTTOM:
                                                if (i_row + 1) < self.data.rowMax:                                        
                                                    processed[i_row + 1][i_col] = origin_cell.value
                                                    is_going = True
                                                    check(i_row_parent, i_col_parent, i_row + 1, i_col, is_going, sheet_obj, processed, direction)
                    else: #cell.value == None:
                        if checkSide(cell, direction):
                            if is_going:
                                if i_row < self.data.rowMax and  i_col < self.data.colMax:                                                                                    
                                    if direction == self.DirectionOfGroupingUp.TOP:
                                        if (i_row - 1) > 1:
                                            processed[i_row - 1][i_col] = origin_cell.value
                                            check(i_row_parent, i_col_parent, i_row - 1, i_col, is_going, sheet_obj, processed, direction)
                                    if direction == self.DirectionOfGroupingUp.BOTTOM:
                                        if (i_row + 1) < self.data.rowMax:                               
                                            processed[i_row + 1][i_col] = origin_cell.value
                                            check(i_row_parent, i_col_parent, i_row + 1, i_col, is_going, sheet_obj, processed, direction)                  
        for i_row in range(1,self.data.rowMax):
            for i_col in range(1, self.data.colMax):
                check(i_row, i_col, i_row, i_col, False, sheet_obj, processed, direction)

    def filterSpaces(self):
        for i_row in range(1,self.data.rowMax):
            for i_col in range(1, self.data.colMax):
                blockStr = self.data.processed[i_row][i_col]
                if (not blockStr) or isinstance(blockStr, int):
                    blockStr = ""
                self.data.processed[i_row][i_col] = " ".join(blockStr.split())

    def readDoc(self, dayOfStartDic):
        if self.worbookNamesCurrent:
            sheet_obj = self.wb_obj[self.worbookNamesCurrent]
        else:
            sheet_obj = self.wb_obj.active
        
        self.dayOfStartDic = dayOfStartDic

        # Избавится от объеденённых ячеек
        self.data.processed = [ [0]*self.data.colMax for i in range(self.data.rowMax)]
        self.unMergeCells(sheet_obj, self.data.processed)
        self.groupUpBorders(sheet_obj, self.data.processed, self.DirectionOfGroupingUp.TOP)
        self.groupUpBorders(sheet_obj, self.data.processed, self.DirectionOfGroupingUp.BOTTOM)

        self.filterSpaces()

        self.parseBorders()

        self.parseData()

        self.calcYear()
    def readHead(self):        
        self.wb_obj = openpyxl.load_workbook(self.docPath)
        self.worbookNames = self.wb_obj.sheetnames
    def __init__(self, docPath):
        super().__init__()
        self.data = InputData()
        self.dataYear = dm.CalenderYear()
        self.rules = dm.Rules()
        self.dayOfStartDic = None

        self.data.rowMax = 100
        self.data.colMax = 25
        self.docPath = docPath

        self.worbookNamesCurrent = None
        self.readHead()
        # To open the workbook 
        # workbook object is created
        #wb_obj = openpyxl.load_workbook(path)

        # Get workbook active sheet object
        # from the active attribute
        #sheet_obj = wb_obj.active        
        
    def getRules(self):
        return self.rules
    def isWeekDayName(self, cell):
        if cell == 'п о н е д е л ь н и к' or cell == 'П о н е д е л ь н и к' or cell == 'понедельник':
            return dm.DayOfWeek.MONDAY
        elif cell == 'в т о р н и к' or cell == 'В т о р н и к' or cell == 'вторник':
            return dm.DayOfWeek.TUESDAY
        elif cell == 'с р е д а' or cell == 'С р е д а' or cell == 'среда':
            return dm.DayOfWeek.WEDNESDAY
        elif cell == 'ч е т в е р г' or cell == 'Ч е т в е р г' or cell == 'четверг':
            return dm.DayOfWeek.THURSDAY
        elif cell == 'п я т н и ц а' or cell == 'П я т н и ц а' or cell == 'пятница':
            return dm.DayOfWeek.FRIDAY
        elif cell == 'с у б б о т а' or cell == 'С у б б о т а' or cell == 'суббота':
            return dm.DayOfWeek.SATURDAY
        else:
            return None
    def isPara(self, cell):
        if 'пара' in cell:
            number = cell[0]
            number = int(number)
            return dm.Para(number)
        else:
            return None
    def isTime(self, cell):
        pattern = r'\d{1,2}\.\d{2}/\d{1,2}\.\d{2}'
        match = re.search(pattern, cell)
        if match:
            splitted = cell.split('/')
            for curr in splitted:
                s = curr.split('.')
                return dt.time(int(s[0]),int(s[1]))
        else:
            return None
    def isGroup(self, cell):
        pattern = r'(.+?)\s+(\d{2})\s*$'
        pattern2 = r'^[С\s]*\d{1,2}[РРЭССКТР\s\-]*\s*\(\d+\)$'
        matches = re.findall(pattern, cell)
        if matches:
            return True
        else:
            matches = re.findall(pattern2, cell)
            if matches:
                return True
        return False 
    def parseBorders(self): 
        # DEBUG
        """calenderDay = dm.CalenderDay(dm.date(2025, 9, 25))

        calenderDay.addBlock(dm.CalenderBlock(dm.Id(1), dt.time(10, 0), dm.Para(1), dm.Auditory("5442"), dm.Subject("Math"), dm.Professor("Big Smoke"), dm.Group("a1")))
        calenderDay.addBlock(dm.CalenderBlock(dm.Id(2), dt.time(10, 0), dm.Para(1), dm.Auditory("5442"), dm.Subject("Music"), dm.Professor("Big Smoke"), dm.Group("a1")))
        calenderDay.addBlock(dm.CalenderBlock(dm.Id(3), dt.time(12, 0), dm.Para(3), dm.Auditory("1442"), dm.Subject("Prog"), dm.Professor("Small di"), dm.Group("a1")))
        calenderDay.addBlock(dm.CalenderBlock(dm.Id(4), dt.time(11, 0), dm.Para(2), dm.Auditory("1442"), dm.Subject("Russian"), dm.Professor("Lol Kek"), dm.Group("a1")))
        calenderDay.addBlock(dm.CalenderBlock(dm.Id(5), dt.time(14, 0), dm.Para(5), dm.Auditory("3442"), dm.Subject("English"), dm.Professor("Abu Hui"), dm.Group("a1")))

        self.dataYear.addDay(calenderDay)"""

        # Пройтись по левой колонке где день и пара/время
        i_row = 0
        readed = False
        self.leftColumnData = []
        while not readed:
            #rowsCurrent, colsCurrent = 4, 50
            #currentRow = [[0 for _ in range(colsCurrent)] for _ in range(rowsCurrent)]
            for j_col in range(15):
                cell = self.data.processed[i_row][j_col]
                weekday = self.isWeekDayName(cell)
                if weekday:
                    cellRightNear = self.data.processed[i_row][j_col + 1]
                    para = self.isPara(cellRightNear)
                    if para:
                        cellRightBottomNear = self.data.processed[i_row + 1][j_col + 1]
                        if self.isTime(cellRightBottomNear):
                            # Сдесь мы в левой верхней границе
                            self.leftColumnData.append({'weekday' : weekday, 'para' : para, 'rows' : (i_row, i_row + 1,)})
            if i_row + 1 < self.data.rowMax:
                i_row += 1
            else:
                readed = True

        # Пройтись по верху где группа
        j_col = 0
        readed = False
        self.topRowData = []
        while not readed:
            for i_row in range(30):
                cell = self.data.processed[i_row][j_col]
                if cell:
                    if self.isGroup(cell):
                        self.topRowData.append({'group' : dm.Group(cell), 'col' : j_col})

            if j_col + 1 < self.data.colMax:
                j_col += 1
            else:
                readed = True

        #self.rules.addRule(dm.Rule(dm.Auditory("5442"), dm.DayOfWeek.MONDAY, dm.Para(1), dm.RuleEven.DEFAULT, None, dm.RuleSubgroup.DEFAULT, dm.Id(1)))
    @staticmethod
    def parseCell(cell):
        if not cell:
            return None
        
        cloneResult  = {'auditory' : None, 'even' : None, 'week' : None, 'subgroup' : None, 'confidence' : None}
        result = []

        confidence = 100

        auditory = None
        even = dm.RuleEven.DEFAULT
        week = []
        subgroup = dm.RuleSubgroup.DEFAULT

        if 'чн.' in cell:
            even = dm.RuleEven.EVEN
            if 'нч.' in cell:
                confidence -= 20
            
        if 'нч.' in cell:
            even = dm.RuleEven.ODD
            if 'чн.' in cell:
                confidence -= 20
        
        comment = cell.replace('чн.','')
        comment = comment.replace('нч.','')

        patternAud = r'[0-9]{4}'
        matches = re.findall(patternAud, cell)
        comment = re.sub(patternAud, "", comment)
        if len(matches) != 1:
            confidence -= 20
        else:
            """auditoryTextWithTrash = matches[0][0] + matches[0][1]

            patternAudNumber = r'(\d+)\s*$'  
            matches = re.findall(patternAudNumber, auditoryTextWithTrash)

            auditoryText = "1000"
            if len(matches) == 1:
                auditoryText = matches[0]
            else:
                confidence -= 20

            if len(auditoryText) != 4:
                confidence -= 20
            """
            auditory = dm.Auditory(int(matches[0]))

        countOfSubgroup = 0
        countOfSubgroup += cell.count('подгр')
        countOfSubgroup += cell.count('п/гр')
        
        
        if countOfSubgroup > 1:
            subgroupRegexp = r"(\d)\s*(?:п/гр\.|подгр)\s*-?\s*([\d,]+)"
            matchesSubGroup = re.findall(subgroupRegexp, cell)
            comment = re.sub(subgroupRegexp, "", comment)
            
            comment = comment.replace('нед', '')
            comment = re.sub(r"\s+", " ", comment).strip()
            
            if len(matchesSubGroup) > 1:
                result.append({'auditory' : auditory, 'even' : even, 'week' : week, 'subgroup' : subgroup, 'confidence' : confidence, 'comment' : comment})
                for match in matchesSubGroup:
                    result.append(result[0].copy())
                    result[-1]['subgroup'] = dm.RuleSubgroup(int(match[0]))
                    result[-1]['week'] = [int(x) if x != '' else 0 for x in match[1].split(',')]
                del result[0]
            else:
                result.append({'auditory' : auditory, 'even' : even, 'week' : week, 'subgroup' : subgroup, 'confidence' : confidence, 'comment' : comment})
        else:
            subgroupRegexp = r'(\d+)\s*(?=п/гр\.|подгр)'
            subgroupMatch = re.findall(subgroupRegexp, cell)
            if len(subgroupMatch) > 0:
                subgroup = dm.RuleSubgroup(int(subgroupMatch[0]))
            else:
                subgroup = dm.RuleSubgroup.DEFAULT
            result.append({'auditory' : auditory, 'even' : even, 'week' : week, 'subgroup' : subgroup, 'confidence' : confidence, 'comment' : comment})
        return result

    def parseData(self):
        # self.leftColumnData
        # self.topRowData
        self.rules = dm.Rules()
        idNum = 1
        for left in self.leftColumnData:
            for top in self.topRowData:
                weekday = left['weekday']
                para = left['para']
                rows = left['rows']
                
                group = top['group']
                col = top['col']

                res1 = self.parseCell(self.data.processed[rows[0]][col])
                res2 = self.parseCell(self.data.processed[rows[1]][col])

                resTotal = []
                if res1:
                    resTotal += res1
                if res2:
                    resTotal += res2

                for rule in resTotal:
                    if rule:
                        self.rules.addRule(dm.Rule(rule['auditory'], weekday, para,  rule['even'],\
                                                   rule['week'], rule['subgroup'], rule['comment'], rule['confidence']))
        pass

    """def GetDataYear(self, year, month, day):
        return self.dataYear"""
    def calcYear(self):
        startDate = dt.datetime(self.dayOfStartDic['year'], self.dayOfStartDic['month'], self.dayOfStartDic['day'])
        endDate = startDate + dt.timedelta(days = 30 * 7)
        currentDate = startDate
        weekStart = startDate.isocalendar().week
        weekNumber = 0
        weekDay = 0

        while currentDate <= endDate:
            weekNumber = currentDate.isocalendar().week - weekStart            
            weekDay = currentDate.weekday()
            print(currentDate.strftime("%Y-%m-%d") + ' ' + f"week: {weekNumber} weekday {weekDay}")            
            
            dayOfWeekEnum = dm.DayOfWeek(weekDay)
            if weekDay % 2 == 0:
                even = dm.RuleEven.EVEN
            else:
                even = dm.RuleEven.ODD

            day = dm.CalenderDay(dt.date(currentDate.year, currentDate.month, currentDate.day))

            for rule in self.rules.rules:
                if rule.dayOfWeek == dayOfWeekEnum:
                    if len(rule.week) == 0:
                        if rule.even != dm.RuleEven.DEFAULT:
                            if rule.even == even:
                                block = dm.CalenderBlock(None, None, rule.para, rule.auditory, rule.subgroup, rule.comment)
                                day.addBlock(block)
                    else:
                        if weekNumber in rule.week:
                            block = block = dm.CalenderBlock(None, None, rule.para, rule.auditory, rule.subgroup, rule.comment)
                            day.addBlock(block) 
            self.dataYear.addDay(day)
            currentDate += dt.timedelta(days=1)


        # day = dm.CalenderDay(dt.date(2025,11,10))
        # block = dm.CalenderBlock(None, dt.time(11,30), dm.Para(1), dm.Auditory(1000))
        #day.addBlock(block)
        #self.dataYear.addDay(day)
    def GetDay(self, year, month, day):
        pass
