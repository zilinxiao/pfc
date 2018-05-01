from traits.api import HasTraits,Range,Enum,List
from traitsui.api import View,Item,HGroup,VGroup,OKButton,CancelButton,\
ApplyButton,RevertButton,Action,Handler,TableEditor
from traitsui.table_column import ObjectColumn
from pyface.api import GUI
from traitsui.table_filter \
    import EvalFilterTemplate, MenuFilterTemplate, RuleFilterTemplate, \
    EvalTableFilter
import numpy as np
class Cable(HasTraits):
    '''
    电缆参数类
    --------------
    主要参数：
    电缆电压U0/U（kV），截面(mm2),电阻（Ω/km),
    电抗（Ω/km),零序电抗(Ω/km),对地电导(s/km),
    电纳（s/km),电容(F/km),电感(H/km),
    零序电感(H/km),电流频率(Hz),电缆芯数
    ------------------
    '''
    u0 = Enum(0.45,0.6,1.8,3.6,6,8.7,12,18,21,26,38,50,64,127,190,290)(26)
    u = Enum(0.75,1,3,6,10,15,20,30,35,66,110,220,330,500)(35)
    s = Range(low=0.0,value=95)
    r = Range(low=0.0,value=0.2465)
    x = Range(low=0.0,value=0.197)
    x0 = Range(low=0.0,value=0.0939)
    g = Range(low=0.0)
    b = Range(low=0.0,value=0.4298e-6)
    c = Range(low=0.0,value=0.1368e-6)
    l = Range(low=0.0,value=0.6279e-3)
    f = Range(low=0.0,value=50.0)
    number = Enum(1,2,3,4,5)(1) 
    def _l_changed(self,old,new):
        self.x = 2.0*np.pi*self.f*new
    def _c_changed(self,old,new):
        self.b = 2.0*np.pi*self.f*new
        
    
    view = View(HGroup(
        VGroup(Item('s',label=u'电缆截面(mm2)'),Item('r',label=u'电阻（Ω）'),
        Item('x',label=u'电抗（Ω)'), Item('x0',label=u'零序电抗（Ω)'),
        Item('g',label=u'对地电导(s)'),Item('b',label=u'对地电纳(s)'),
        show_border=True),
        VGroup(Item('u0',label=u'相电压（kV）'),Item('u',label=u'额定电压（kV）'),
        Item('number',label=u'电缆芯数'),Item('f',label=u'电源频率(Hz)'),
        Item('l',label=u'电感（H/km)'),Item('c',label=u'对地电容(F)'),
        show_border=True),padding = 10),title=u'电缆参数设置',resizable = True,
        buttons =[Action(name='确定',action='ok'),
        Action(name='取消',action='cancel')])


class CableHandler(Handler):
    def ok(self,info):
        info.ui.dispose(True)
    def cancel(self,info):
        info.ui.dispose(False)
    def closed(self,info,is_ok):
        super(CableHandler,self).closed(info,is_ok)
        GUI().stop_event_loop()        
        return is_ok
def f1():
    cb = Cable()
    if cb.configure_traits(handler=CableHandler):
        print(cb.x)
    print(cb.x)

cableArgs_table = TableEditor(
    columns=[ObjectColumn(name = 's',label='电缆截面(mm2)',width = 0.1),
        ObjectColumn(name = 'r',label='电阻（Ω）',width = 0.1),
        ObjectColumn(name = 'x',label='电抗（Ω)',width = 0.1),
        ObjectColumn(name = 'x0',label='零序电抗（Ω)',width = 0.1),
        ObjectColumn(name = 'g',label='对地电导(s)',width = 0.1),
        ObjectColumn(name = 'b',label='对地电纳(s)',width = 0.1)],
    deletable=True,
    sort_model=True,
    auto_size=False,
    orientation='vertical',        
    edit_view=View(
        HGroup(
            VGroup(Item('s',label=u'电缆截面(mm2)'),Item('r',label=u'电阻（Ω）'),
                Item('x',label=u'电抗（Ω)'), Item('x0',label=u'零序电抗（Ω)'),
                Item('g',label=u'对地电导(s)'),Item('b',label=u'对地电纳(s)'),
                show_border=True),
            VGroup(Item('u0',label=u'相电压（kV）'),Item('u',label=u'额定电压（kV）'),
                Item('number',label=u'电缆芯数'),Item('f',label=u'电源频率(Hz)'),
                Item('l',label=u'电感（H/km)'),Item('c',label=u'对地电容(F)'),
                show_border=True),
            padding = 5),
        resizable = True),
    row_factory=Cable)
    
class CableArgsTable(HasTraits):
    cables = List(Cable)
    view = View(
        VGroup(
            Item('cables',
                 show_label=False,
                 editor=cableArgs_table
                 ),
            show_border=True,
        ),
        title='电缆参数设置',
        width=.6,
        height=.6,
        resizable=True,
        buttons =[Action(name='添加',action='addItem'),
        Action(name='删除',action='delItem'),
        Action(name='确定',action='ok'),
        Action(name='取消',action='cancel')],
        kind='live'
    )
class CablesHandler(Handler):
    def addItem(self,info):
        print("addItem")
    def delItem(self,info):
        print('delItem')
    def ok(self,info):
        info.ui.dispose(True)
    def cancel(self,info):
        info.ui.dispose(False)
    def closed(self,info,is_ok):
        super(CableHandler,self).closed(info,is_ok)
        GUI().stop_event_loop()        
        return is_ok
def f2():
    cableargstable = CableArgsTable()
    cableargstable.configure_traits()
f2()



