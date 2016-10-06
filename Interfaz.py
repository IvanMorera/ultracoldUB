# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 15:14:44 2016

@author: ivan
"""
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import loadUiType
Ui_MainWindow,QMainWindow=loadUiType('Main.ui')

class Main(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Main,self).__init__()
        self.setupUi(self)
        self.button1.clicked.connect(self.darkbutton)
        self.button2.clicked.connect(self.brightbutton)
        self.button3.clicked.connect(self.dispersionbutton)
        
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap('initial.png'))
        self.DS.setScene(scene)
    
        self.DS.show()
        
    def darkbutton(self):
        self.hide()
        self.dark_window = DS(self)
        self.dark_window.show()
        self.dark_window.raise_()
    
    def brightbutton(self):
        self.hide()
        self.bright_window = BS(self)
        self.bright_window.show()
        self.bright_window.raise_()   
        
    def dispersionbutton(self):
        self.hide()
        self.dispersion_window = WD(self)
        self.dispersion_window.show()
        self.dispersion_window.raise_()   
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'EXIT',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
          
          
Ui_MainWindow,QMainWindow=loadUiType('DS.ui')
import os
import subprocess

from PyQt4 import QtGui, QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
class DS(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
#        self.mplfigs.hide()
#        self.mplwindow.hide()
        self.ButtonOn.hide()
        self.ButtonBack.hide()
        self.ButtonPause.hide()
        self.start.clicked.connect(self.start1)
        self.back.clicked.connect(self.close)
        self.ButtonOn.clicked.connect(self.on)
        self.ButtonBack.clicked.connect(self.back1)
        self.ButtonPause.clicked.connect(self.pause)        
        self.fig_dict={}
        
        self.mplfigs.itemClicked.connect(self.changefig)
        self.label_5.hide()
        self.slider_simulation.hide()
        self.horizontalSlider.valueChanged.connect(self.initial)
        self.slider_simulation.valueChanged.connect(self.simulation)
        
        file=open('position_0.txt','r')
        lines=file.readlines()
        file.close()
        x=[]
        x1=[]
        for line in lines:
            p=line.split()
            x.append(float(p[0]))
            x1.append(float(p[1]))
        xv=np.array(x)
        xv1=np.array(x1)
        
        self.fig=Figure()
        axf=self.fig.add_subplot(111)
        axf.set_xlabel('$x/a_{ho}$',fontsize=17)
        axf.set_ylabel('density $|\psi|^2$',fontsize=14)
        axf.plot(xv,xv1)
        axf.set_title('condensate')
        self.addmpl(self.fig) 
            
    
    def initial(self):
        file=open('initial.txt','r')
        lines=file.readlines()
        file.close()
        for i in range(1,13):
            globals()['x%s' %i]=[]
        for line in lines:
            p=line.split()
            for i in range(1,13):
                globals()['x%s' %i].append(float(p[i-1]))
        for i in range(1,13):
                globals()['xv%s' %i]=np.array(globals()['x%s' %i])       
        value=self.horizontalSlider.value()
        
        for i in range(2,13):
            if value==i-7:
                if self.fig==None:
                    self.rmmpl()
                    self.fig=Figure()
                    self.addmpl(self.fig)
                    
                
                self.fig.clear()
                ax1f2=self.fig.add_subplot(111)
                ax1f2.set_xlabel('$x/a_{ho}$',fontsize=17)
                ax1f2.set_ylabel('density $|\psi|^2$',fontsize=14)
                ax1f2.plot(xv1,globals()['xv%s' %i])
                ax1f2.set_title('initial state')
                self.canvas.draw()

    def changefig(self,item):
        text=item.text()
        self.rmmpl()
        self.addmpl(self.fig_dict[str(text)])
        self.fig=None
        
    def addfig(self,name,fig):
        self.fig_dict[name]=fig
        self.mplfigs.addItem(name)
        
    def delfig(self):
        listItems=self.mplfigs.selectedItems()
        if not listItems: return
        for item in listItems:
            self.mplfigs.takeItem(self.mplfigs.row(item))
            
    def addmpl(self,fig):
        self.canvas=FigureCanvas(fig)
        self.toolbar=NavigationToolbar(self.canvas,self,coordinates=True)
        self.mplvl.addWidget(self.toolbar)        
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()


    def plot(self):
        prevdir = os.getcwd()
        try:
            os.chdir(os.path.expanduser('./darksolitons'))
            self.slider_simulation.value()
            file=open('WfDs-%08d.txt'%(self.sim),'r')
            globals()['lines%s' %self.sim]=file.readlines()
            file.close()
            x1=[]
            x2=[]
            for line in (globals()['lines%s' %self.sim]):
                p=line.split()
                x1.append(float(p[0]))
                x2.append(float(p[1]))
            xv1=np.array(x1)
            xv2=np.array(x2)
                
        finally:
            os.chdir(prevdir)
        if self.fig==None:
            self.rmmpl()
            self.fig=Figure()
            self.addmpl(self.fig)    
        self.fig.clear()
        axf=self.fig.add_subplot(111)
        axf.set_xlabel('$x/a_{ho}$',fontsize=17)
        axf.set_ylabel('density $|\psi|^2$',fontsize=14)
        axf.plot(xv1,xv2)
        axf.set_title('state at %s' %(self.sim))
        self.canvas.draw()
        
        if (self.sim==self.spinBox.value()*int((10*np.pi*np.sqrt(2.)))-1):
            self.timer.stop()
            
    def plot2(self):
        prevdir = os.getcwd()
        try:
            os.chdir(os.path.expanduser('./darksolitons'))
            self.sim-=1
            file=open('WfDs-%08d.txt'%(self.sim),'r')
            globals()['lines%s' %self.sim]=file.readlines()
            file.close()
            x1=[]
            x2=[]
            for line in (globals()['lines%s' %self.sim]):
                p=line.split()
                x1.append(float(p[0]))
                x2.append(float(p[1]))
            xv1=np.array(x1)
            xv2=np.array(x2)
                
        finally:
            os.chdir(prevdir)
        if self.fig==None:
            self.rmmpl()
            self.fig=Figure()
            self.addmpl(self.fig)    
        self.fig.clear()
        axf=self.fig.add_subplot(111)
        axf.set_xlabel('$x/a_{ho}$',fontsize=17)
        axf.set_ylabel('density $|\psi|^2$',fontsize=14)
        axf.plot(xv1,xv2)
        axf.set_title('state at %s' %(self.sim))
        self.canvas.draw()
        if (self.sim==1):
            self.timer.stop()
            
    def on(self):
        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.plot)
        self.timer.start(250)
    
    def pause(self):
        self.timer.stop()
        
    def back1(self):
        self.timer.timeout.connect(self.plot2)
        self.timer.start(75)


    def start1(self):
        self.sim=0
        prevdir = os.getcwd()
        try:
            os.chdir(os.path.expanduser('./darksolitons'))
            file=open('input.txt','w')  
            file.write ('%s\t%s' %(self.horizontalSlider.value(),self.spinBox.value()))
            file.close()
            subprocess.call('python gpe_fft_ts_DS_v1.py',shell=True)
            print (os.getcwd())
            time.sleep(70.0*self.spinBox.value())
            print ("READY")
            self.label_5.show()
            self.ButtonOn.show()
            self.ButtonBack.show()
            self.ButtonPause.show()
            self.slider_simulation.show()
            self.slider_simulation.setMinimum(0)
            self.slider_simulation.setMaximum(self.spinBox.value()*int((10*np.pi*np.sqrt(2.)))-1)
            self.slider_simulation.setSingleStep(1)
        
            file = open('energies.txt', 'r')
            lines = file.readlines()
            file.close()
            file2=open('phase.txt','r')
            lines2=file2.readlines()
            file2.close()
            file3=open('min.txt','r')
            lines3=file3.readlines()
            file3.close()
        finally:
            os.chdir(prevdir)
            
        
        x2 = []
        y2 = []
        for line in lines2:
            p2 = line.split()
            x2.append(float(p2[0]))
            y2.append(float(p2[1]))
        xv2 = np.array(x2)
        yv2 = np.array(y2)
        fig1=Figure()
        ax1f1=fig1.add_subplot(111)
        ax1f1.set_ylabel('PHASE',fontsize=14)
        ax1f1.set_xlabel('$T/t_{ho}$',fontsize=17)        
        ax1f1.plot(xv2,yv2, 'b.-')
        ax1f1.set_title('Phase difference produced by soliton')
      


        
        x1 = []
        y1 = []
        z1 = []
        for line in lines:
            p = line.split()
            x1.append(float(p[0]))
            y1.append(float(p[1]))
            z1.append(float(p[2]))                            
        xv = np.array(x1)
        yv = np.array(y1)
        zv = np.array(z1)
        
        fig2=Figure()
        ax1f2=fig2.add_subplot(121)
        ax1f2.set_xlabel('$T/t_{ho}$',fontsize=17)        
        ax1f2.set_ylabel('$E/hw$',fontsize=17)
        ax1f2.plot(xv,yv, 'b.-')
        ax1f2.set_title('Medium Energy')
        
        ax2f2=fig2.add_subplot(122)
        ax2f2.set_xlabel('$T/t_{ho}$',fontsize=17)
        ax2f2.plot(xv,zv, 'r.-')
        ax2f2.set_title('Chemical Potential')
       
        
        
        x3 = []
        y3 = []
        for line in lines3:
            p3 = line.split()
            x3.append(float(p3[0]))
            y3.append(float(p3[1]))
        xv3 = np.array(x3)
        yv3 = np.array(y3)
        
        fig3=Figure()
        ax1f3=fig3.add_subplot(111)
        ax1f3.set_xlabel('$T/t_{ho}$',fontsize=17)        
        ax1f3.set_ylabel('$x/a_{ho}$',fontsize=17)
        ax1f3.plot(xv3,yv3,'b.-')
        ax1f3.set_title('Soliton Position')

        
        
        self.delfig()
        self.delfig()
        self.delfig()
        self.addfig('PHASE',fig1)
        self.addfig('ENERGY',fig2)
        self.addfig('MINUS',fig3)
        
                
    def simulation(self):
        time=self.spinBox.value()*int((10*np.pi*np.sqrt(2.)))-1
        value=self.slider_simulation.value()
        prevdir = os.getcwd()
        try:
            os.chdir(os.path.expanduser('./darksolitons'))
            for i in range(1,time+1):
                file=open('WfDs-%08d.txt'%(i),'r')
                globals()['lines%s' %i]=file.readlines()
                file.close()
#            
#            
                if value==i:                    
                    x1=[]
                    x2=[]
                    for line in (globals()['lines%s' %i]):
                        p=line.split()
                        x1.append(float(p[0]))
                        x2.append(float(p[1]))
                    xv1=np.array(x1)
                    xv2=np.array(x2)
                    
                    if self.fig==None:
                        self.rmmpl()
                        self.fig=Figure()
                        self.addmpl(self.fig)
                    self.fig.clear()
                    axf=self.fig.add_subplot(111)
                    axf.set_xlabel('$x/a_{ho}$',fontsize=17)
                    axf.set_ylabel('density $|\psi|^2$',fontsize=14)
                    axf.plot(xv1,xv2)
                    axf.set_title('state at %s' %(i))
                    self.canvas.draw()
        finally:
            os.chdir(prevdir)
            
            
    def rmmpl(self):
        self.mplvl.removeWidget(self.toolbar)
        self.canvas.close()        
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        
                
    def close(self):
        self.hide()
        self.parent().show()
            
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'EXIT',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
 
 
Ui_MainWindow,QMainWindow=loadUiType('BS.ui')

class BS(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.ButtonOn.hide() #amaguem tots els sliders o botons no necessaris pel moment
        self.ButtonBack.hide()
        self.ButtonPause.hide()
        self.harm.hide() #seguim amagant coses no necessaries pel moment
        self.none.hide()
        self.wall.hide()
        self.label_5.hide()
        self.slider_simulation.hide()
        
        #let's give the possible values to sliders
        self.horizontalSlider_4.setMinimum(-60)
        self.horizontalSlider_4.setMaximum(-20)
        self.horizontalSlider_4.setSingleStep(1)
        self.horizontalSlider_4.TicksBelow
        
        self.btn_none.clicked.connect(self.V_none)
        self.btn_harm.clicked.connect(self.V_harm)
        self.btn_wall.clicked.connect(self.V_wall)

        self.fig_dict={}
        
        self.mplfigs.itemClicked.connect(self.changefig)

        self.fig=Figure()
        self.addmpl(self.fig)   
        
        self.start.clicked.connect(self.start2) #despres definirem start1 que ens dona les dades inicials
        self.back.clicked.connect(self.close)
        
    def addmpl(self,fig):
        self.canvas=FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar=NavigationToolbar(self.canvas,self.mpl_window,coordinates=True)
        self.mplvl.addWidget(self.toolbar)
        
    def rmmpl(self,):
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        self.mplvl.removeWidget(self.toolbar)
        self.toolbar.close()
        
    def addfig(self,name,fig):
        self.fig_dict[name]=fig
        self.mplfigs.addItem(name)
        
    def changefig(self,item):
        text=item.text()
        self.rmmpl()
        self.addmpl(self.fig_dict[str(text)])
        
    def V_none(self):
        file_pot=open('pot_input.txt','w')
        file_pot.write('%d' %(0))
        file_pot.close()
        
    def V_harm(self):
        file_pot=open('pot_input.txt','w')
        file_pot.write('%d' %(1))
        file_pot.close()
        
    def V_wall(self):
        file_pot=open('pot_input.txt','w')
        file_pot.write('%d' %(2))
        file_pot.close()
        
    def start2(self):
        pot_file=open('pot_input.txt','r')
        prevdir=os.getcwd()
        try:
            os.chdir(os.path.expanduser('./brightsolitons'))
            pot=int((pot_file.readlines())[0])
            file_data=open('input.txt','w')
            if pot==0:           
                file_data.write('%d \t %d \t %f \t %f \t %d' %(0,self.gn.value(),self.horizontalSlider.value(),self.horizontalSlider_2.value(),self.yes_no.value()))
            elif pot==1:
                file_data.write('%d \t %d \t %f \t %d \t %d' %(1,self.gn.value(),self.horizontalSlider_3.value(),self.spinBox.value(),0))
            elif pot==2:
                file_data.write('%d \t %d \t %f \t %f \t %d \t %d \t %f' %(2,self.gn.value(),self.horizontalSlider_4.value(),self.horizontalSlider_5.value(),self.yes_no.value(),0.5*(2**self.wb.value()),self.hb.value()/10.0))
            file_data.close()
            pot_file.close()
            subprocess.Popen('python gpe_bright_solitons.py',shell=True) #we run our code with the input already written
            if pot==0 or pot==2:
                time.sleep(80.0)
            elif pot==1:
                time.sleep(80.0*self.spinBox.value())
            #let's read the ouput files to plot the data            
            energyfile=open('./bs_evolution/energies.dat','r')
            energy=energyfile.readlines()
            energyfile.close()
            meanvalfile=open('./bs_evolution/meanvalues.dat','r')
            meanval=meanvalfile.readlines()
            meanvalfile.close()
        
        finally:
            os.chdir(prevdir)
                        
        #meanvalues (1st line of the data file is information)
        tmv=[] #time
        mv=[]  #mean value
        smv=[] #sigma
        for i in xrange(1,len(meanval)):
            tmv.append(float((meanval[i].split('\t'))[0]))
            mv.append(float((meanval[i].split('\t'))[1]))
            smv.append(float((meanval[i].split('\t'))[2]))
        fig1=Figure()
        figmv=fig1.add_subplot(111) #only one plot in the window
        atmv=np.array(tmv)
        amv=np.array(mv)
        figmv.plot(atmv,amv)
        if pot==1:
            figmv.axes.set_xlim([0,2*np.pi*self.spinBox.value()])
            figmv.axes.set_ylim([-36.0,36.0])
        else:
            figmv.axes.set_xlim([0,20.0])
            figmv.axes.set_ylim([-128.0,128.0])
        figmv.set_title("Position of the soliton")
        figmv.set_xlabel("Time ($s$)")
        figmv.set_ylabel("Position")
            
        #energies
        ftime=[]
        etot=[]
        chem=[]
        ekin=[]
        epot=[]
        eint=[]
        lint=[]
        iint=[]
        rint=[]
        for i in xrange(1,len(energy)):
            ftime.append(float((energy[i].split('\t'))[0]))
            etot.append(float((energy[i].split('\t'))[1]))
            chem.append(float((energy[i].split('\t'))[2]))
            ekin.append(float((energy[i].split('\t'))[3]))
            epot.append(float((energy[i].split('\t'))[4]))
            eint.append(float((energy[i].split('\t'))[5]))
            if pot==2:
                lint.append(float((energy[i].split('\t'))[6]))
                iint.append(float((energy[i].split('\t'))[7]))
                rint.append(float((energy[i].split('\t'))[8]))
            else:
                pass
                
        fig2=Figure()
        fig3=Figure()
          
        atime=np.array(ftime)
        aetot=np.array(etot)
        achem=np.array(chem)
        aekin=np.array(ekin)
        aepot=np.array(epot)
        aeint=np.array(eint)
        if pot==2:
            alint=np.array(lint)
            aiint=np.array(iint)
            arint=np.array(rint)
        else:
            pass
           
        if pot==1:
            allenergies=fig2.add_subplot(111)
#            kinpot=fig2.add_subplot(122)
            allenergies.plot(atime,aetot,label='$E_{tot}$')
            allenergies.plot(atime,achem,label='$\mu$')
            allenergies.plot(atime,aekin,label='$E_{kin}$')
            allenergies.plot(atime,aepot,label='$E_{pot}$')
            allenergies.plot(atime,aeint,label='$E_{int}$')
            allenergies.axes.set_xlim([0,2*np.pi*self.spinBox.value()])
 #           kinpot.plot(atime,aetot,label='$E_{tot}$')
 #           kinpot.plot(atime,aepot,label='$e_{pot}$')
 #           kinpot.plot(atime,aekin,label='$E_{kin}$')
 #           kinpot.axes.set_xlim([0,2*np.pi*self.spinBox.value()])
        else:
            allenergies=fig2.add_subplot(111)
            allenergies.plot(atime,aetot,label='$E_{tot}$')
            allenergies.plot(atime,achem,label='$\mu$')
            allenergies.plot(atime,aekin,label='$E_{kin}$')
            allenergies.plot(atime,aepot,label='$E_{pot}$')
            allenergies.plot(atime,aeint,label='$E_{int}$')
            if pot==2:
                integrals=fig3.add_subplot(111)
                integrals.plot(atime,alint,label='left side')
                integrals.plot(atime,aiint,label='inside')
                integrals.plot(atime,arint,label='right side')
          
  #      self.delfig()
  #      self.delfig()
        if pot==2:
  #          self.delfig()
            self.addfig("Integral",fig3)
        else:
            pass
        self.addfig("Position's mean value", fig1)
        self.addfig("Energies",fig2)
        

    def close(self):
        self.hide()
        self.parent().show()
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'EXIT',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
         
Ui_MainWindow,QMainWindow=loadUiType('WD.ui')
class WD(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.back.clicked.connect(self.close)

    def close(self):
        self.hide()
        self.parent().show()
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'EXIT',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        
if __name__=='__main__':
    import sys
    from PyQt4 import QtGui
    import numpy as np
    
    
    app=QtGui.QApplication(sys.argv)
    main=Main()
    main.show()
    sys.exit(app.exec_())
