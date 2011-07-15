#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
"""Skrypt umożliwiający dodanie nowego modelu do danego modułu w magento

Wykorzystanie: add_model.py -p nazwa_pakietu -m nazwa_modułu -t nazwa_tabeli nazwa_modelu

Opcje:
  -p ...   wykorzystuje konkretny pakiet (WYMAGANE)
  -m ...   wykorzystuje konkretny moduł (WYMAGANE)
  -t ...   nazwa tabeli w bazie danych (WYMAGANE)

  -h       wyświetla pomoc

"""

__author__ = "Kamil Szymczyk"

import sys
import getopt
import os
from xml.dom import minidom


class Module:
    """Klasa reprezentująca moduł
    """
    
    def __init__(self, package, module):
        self.package = package
        self.module = module
        self.setModulePath()
        self.parseConfigFile()
        
    def setModulePath(self):
        """ Ustawia ścieżkę do modułu
        """
        self.modulePath = os.path.join('app/code/local/', self.package, self.module)

    def parseConfigFile(self):
        """Wczytuje i parsuje plik config.xml modułu
        
        Arguments:
        - `self`:
        """
        self.config = minidom.parse(os.path.join(self.modulePath, 'etc/config.xml'))

    def addModel(self, model, table):
        """Funkcja dodająca model do danego modułu
           UWAGA: na ten moment działa tylko wtedy, gdy nie istnieje pierwotny model.
                  występuje jakiś problem z wyciągniem przez getElementsByTagName
                  NodeList zamiast konkretnego Elementu
        
        Arguments:
        - `model`: nazwa modelu, który ma zostać dodany
        """
        # TODO zrefaktorować tworzenie podstaw modelu do innej metody
        globalTag = self.config.getElementsByTagName('global')
        if not globalTag:
            print 'Nie ma tagu "global", skrypt tworzy nowy...'
            globalTag = self.config.createElement('global')
            self.config.documentElement.appendChild(globalTag)
            self.config.documentElement.appendChild(self.config.createTextNode('\n'))
        else:
            globalTag = globalTag[0]
        modelsTag = self.config.getElementsByTagName('models')
        if not modelsTag:
            print 'Nie ma tagu "models", skrypt tworzy nowy...'
            modelsTag = self.config.createElement('models')
            globalTag.appendChild(self.config.createTextNode('\n'))
            globalTag.appendChild(modelsTag)
            globalTag.appendChild(self.config.createTextNode('\n'))
        else:
            modelsTag = modelsTag[0]
        moduleTag = modelsTag.getElementsByTagName(self.module.lower())
        if not moduleTag:
            moduleTag = self.config.createElement(self.module.lower())
            modelsTag.appendChild(self.config.createTextNode('\n'))
            modelsTag.appendChild(moduleTag)
            modelsTag.appendChild(self.config.createTextNode('\n'))
            classTag = self.config.createElement('class')
            classTag.appendChild(self.config.createTextNode('_'.join([self.package, self.module, 'Model'])))
            moduleTag.appendChild(self.config.createTextNode('\n'))
            moduleTag.appendChild(classTag)
            moduleTag.appendChild(self.config.createTextNode('\n'))
            resourceModelTag = self.config.createElement('resourceModel')
            resourceModelTag.appendChild(self.config.createTextNode('_'.join([self.module.lower(), 'mysql4'])))
            moduleTag.appendChild(resourceModelTag)
            moduleTag.appendChild(self.config.createTextNode('\n'))
        else:
            moduleTag = moduleTag[0]
        modelResourceModelTag = modelsTag.getElementsByTagName(self.module.lower()+'_mysql4')
        if not modelResourceModelTag:
            modelResourceModelTag = self.config.createElement(self.module.lower()+'_mysql4')
            modelsTag.appendChild(modelResourceModelTag)
            modelsTag.appendChild(self.config.createTextNode('\n'))
            classTag2 = self.config.createElement('class')
            classTag2.appendChild(self.config.createTextNode('_'.join([self.package, self.module, 'Model', 'Mysql4'])))
            modelResourceModelTag.appendChild(self.config.createTextNode('\n'))
            modelResourceModelTag.appendChild(classTag2)
            modelResourceModelTag.appendChild(self.config.createTextNode('\n'))
            entitiesTag = self.config.createElement('entities')
            modelResourceModelTag.appendChild(entitiesTag)
            modelResourceModelTag.appendChild(self.config.createTextNode('\n'))
        else:
            modelResourceModelTag = modelResourceModelTag[0]
        resourcesTag = globalTag.getElementsByTagName('resources')
        if not resourcesTag:
            resourcesTag = self.config.createElement('resources')
            globalTag.appendChild(resourcesTag)
            globalTag.appendChild(self.config.createTextNode('\n'))
            # moduł zapisu
            moduleWriteTag = self.config.createElement(self.module.lower()+'_write')
            resourcesTag.appendChild(self.config.createTextNode('\n'))
            resourcesTag.appendChild(moduleWriteTag)
            resourcesTag.appendChild(self.config.createTextNode('\n'))
            connectionTag = self.config.createElement('connection')
            moduleWriteTag.appendChild(self.config.createTextNode('\n'))
            moduleWriteTag.appendChild(connectionTag)
            moduleWriteTag.appendChild(self.config.createTextNode('\n'))
            useTag = self.config.createElement('use')
            useTag.appendChild(self.config.createTextNode('core_write'))
            connectionTag.appendChild(self.config.createTextNode('\n'))
            connectionTag.appendChild(useTag)
            connectionTag.appendChild(self.config.createTextNode('\n'))
            # moduł odczytu
            moduleReadTag = self.config.createElement(self.module.lower()+'_read')
            resourcesTag.appendChild(moduleReadTag)
            resourcesTag.appendChild(self.config.createTextNode('\n'))
            connectionTag2 = self.config.createElement('connection')
            moduleReadTag.appendChild(self.config.createTextNode('\n'))
            moduleReadTag.appendChild(connectionTag2)
            moduleReadTag.appendChild(self.config.createTextNode('\n'))
            useTag2 = self.config.createElement('use')
            useTag2.appendChild(self.config.createTextNode('core_read'))
            connectionTag2.appendChild(self.config.createTextNode('\n'))
            connectionTag2.appendChild(useTag2)
            connectionTag2.appendChild(self.config.createTextNode('\n'))
        else:
            resourcesTag = resourcesTag[0]
        
        # skoro już tu jestem to wartu dorzucić konfigruację setupu
        moduleSetupTag = resourcesTag.getElementsByTagName(self.module.lower()+'_setup')
        if not moduleSetupTag:
            moduleSetupTag = self.config.createElement(self.module.lower()+'_setup')
            setupTag = self.config.createElement('setup')
            moduleSetupTag.appendChild(self.config.createTextNode('\n'))
            moduleSetupTag.appendChild(setupTag)
            moduleSetupTag.appendChild(self.config.createTextNode('\n'))
            setupModuleTag = self.config.createElement('module')
            setupModuleTag.appendChild(self.config.createTextNode('_'.join([self.package, self.module])))
            setupClassTag = self.config.createElement('class')
            setupClassTag.appendChild(self.config.createTextNode('_'.join([self.package, self.module, 'Model_Resource_Mysql4_Setup'])))
            setupTag.appendChild(self.config.createTextNode('\n'))
            setupTag.appendChild(setupModuleTag)
            setupTag.appendChild(self.config.createTextNode('\n'))
            setupTag.appendChild(setupClassTag)
            setupTag.appendChild(self.config.createTextNode('\n'))
            setupConnectionTag = self.config.createElement('connection')
            moduleSetupTag.appendChild(setupConnectionTag)
            moduleSetupTag.appendChild(self.config.createTextNode('\n'))
            setupUseTag = self.config.createElement('use')
            setupUseTag.appendChild(self.config.createTextNode('core_setup'))
            setupConnectionTag.appendChild(self.config.createTextNode('\n'))
            setupConnectionTag.appendChild(setupUseTag)
            setupConnectionTag.appendChild(self.config.createTextNode('\n'))
            resourcesTag.appendChild(moduleSetupTag)
            resourcesTag.appendChild(self.config.createTextNode('\n'))
        else:
            moduleSetupTag = moduleSetupTag[0]
            
        try:
            os.makedirs(os.path.join(self.modulePath, 'Model', 'Resource', 'Mysql4'))
        except OSError:
            pass
        mysqlModelFile = open(os.path.join(self.modulePath, 'Model', 'Resource', 'Mysql4', 'Setup.php'), 'w')
        mysqlModelFileText = '<?php\n\nclass '+self.package+'_'+self.module+'_Model_Resource_Mysql4_Setup extends Mage_Core_Model_Resource_Setup {'
        mysqlModelFileText += '\n  protected function _construct() {'
        mysqlModelFileText += '\n    $this->_init(\''+self.module.lower()+'/'+model+'\', \''+model+'_id\');'
        mysqlModelFileText += '\n  }'
        mysqlModelFileText += '\n}'

        mysqlModelFile.write(mysqlModelFileText)
        mysqlModelFile.close()

        installScriptFilePath = os.path.join(self.modulePath, 'sql', self.module.lower()+'_setup', 'mysql4-install-0.1.0.php')
        if not (os.path.exists(installScriptFilePath)):
            try:
                os.mkdir(os.path.join(self.modulePath, 'sql', self.module.lower()+'_setup'))
            except OSError:
                pass
            installFile = open(installScriptFilePath, 'w')
            installFileText = '<?php\n\n'
            installFileText += '$installer = $this;'
            installFileText += '\n$installer->startSetup();'
            installFileText += '\n\n$installer->endSetup();'
            installFile.write(installFileText)
            installFile.close()

        # fragment zajmujący się faktycznie wstawianiem modelu (zrobiony tak żeby się za bardzo nie integrował
        # z kodem inicjalizacyjnym)
        modelResourceModelTag = modelsTag.getElementsByTagName(self.module.lower()+'_mysql4')
        if not modelResourceModelTag:
            print 'Coś się spaprało przy ręcznej generacji pliku modelu'
            sys.exit(2)
        else:
            modelResourceModelTag = modelResourceModelTag[0]
        entitiesTag = modelResourceModelTag.getElementsByTagName('entities')
        if not entitiesTag:
            print 'Coś się spaprało przy ręcznej generacji pliku modelu'
            sys.exit(2)
        else:
            entitiesTag = entitiesTag[0]
        currentModelTag = self.config.createElement(model)
        tableTag = self.config.createElement('table')
        tableTag.appendChild(self.config.createTextNode(table))
        currentModelTag.appendChild(self.config.createTextNode('\n'))
        currentModelTag.appendChild(tableTag)
        currentModelTag.appendChild(self.config.createTextNode('\n'))
        entitiesTag.appendChild(self.config.createTextNode('\n'))
        entitiesTag.appendChild(currentModelTag)
        entitiesTag.appendChild(self.config.createTextNode('\n'))
        
        # print self.config.toxml()       # linijka sprawdzająca, potem się ją zastąpi zapisem
        # sys.exit(0)
        
        with open(os.path.join(self.modulePath, 'etc/config.xml'), 'wb') as configFile:
            self.config.writexml(configFile, indent='', newl='', encoding='utf-8')
        
        modelFile = open(os.path.join(self.modulePath, 'Model', model.capitalize()+'.php'), 'w')
        modelFileText = '<?php\n\nclass '+self.package+'_'+self.module+'_Model_'+model.capitalize()+' extends Mage_Core_Model_Abstract {'
        modelFileText += '\n  protected function _construct() {'
        modelFileText += '\n    $this->_init(\''+self.module.lower()+'/'+model+'\');'
        modelFileText += '\n  }'
        modelFileText += '\n}'
        # print modelFileText
        modelFile.write(modelFileText)
        modelFile.close()

        try:
            os.mkdir(os.path.join(self.modulePath, 'Model', 'Mysql4'))
        except OSError:
            pass # ten katalog mógł zostać stworzony wcześniej, nie ma czym się przejmować
        mysqlModelFile = open(os.path.join(self.modulePath, 'Model', 'Mysql4', model.capitalize()+'.php'), 'w')
        mysqlModelFileText = '<?php\n\nclass '+self.package+'_'+self.module+'_Model_Mysql4_'+model.capitalize()+' extends Mage_Core_Model_Mysql4_Abstract {'
        mysqlModelFileText += '\n  protected function _construct() {'
        mysqlModelFileText += '\n    $this->_init(\''+self.module.lower()+'/'+model+'\', \''+model+'_id\');'
        mysqlModelFileText += '\n  }'
        mysqlModelFileText += '\n}'

        mysqlModelFile.write(mysqlModelFileText)
        mysqlModelFile.close()

        try:
            os.mkdir(os.path.join(self.modulePath, 'Model', 'Mysql4', model.capitalize()))
        except OSError:
            pass # ten katalog mógł zostać stworzony wcześniej, nie ma czym się przejmować
        collectionFile = open(os.path.join(self.modulePath, 'Model', 'Mysql4', model.capitalize(), 'Collection.php'), 'w')
        collectionFileText = '<?php\n\nclass '+self.package+'_'+self.module+'_Model_Mysql4_'+model.capitalize()+'_Collection extends Mage_Core_Model_Mysql4_Collection_Abstract {'
        collectionFileText += '\n  protected function _construct() {'
        collectionFileText += '\n    $this->_init(\''+self.module.lower()+'/'+model+'\');'
        collectionFileText += '\n  }'
        collectionFileText += '\n}'
        # print collectionFileText
        collectionFile.write(collectionFileText)
        collectionFile.close()

def warning():
    """Wyświetla ostrzeżenie
    """
    print 'UWAGA: skrypt stworzy pusty plik konfiguracyjny (w katalogu [modul]/sql/[downcasowanana_nazwa_modulu]_setup/mysql4-install-0.1.0.php)'
    print 'ale jego wypełnienie nie jest zautomatyzowane i musi zostać wykonane ręcznie.'
    print 'Skrypt z automatu przyjmuje nazwę klucza głównego modelu jako [nazwa_modelu]_id. Jeśli ma być ona inna to należy ręcznie wyedytować plik'
    print 'app/code/local/[pakiet]/[moduł]/Model/Mysql4/[nazwa_modelu].php'


def usage():
    """Drukuje dokumentację
    """
    print __doc__
    warning()
    
def main(argv):
    """Funkcja główna
    """
    package = None
    module = None
    table = None
    try:
        opts, args = getopt.getopt(argv, "p:m:t:h")
    except getopt.GetoptError:
        usage()
        print 'Błąd opcji'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt == '-p':
            package = arg
        elif opt == '-m':
            module = arg
        elif opt == '-t':
            table = arg

    if not package:
        usage()
        print 'Nie zdefiniowałeś pakietu'
        sys.exit(2)
    if not module:
        usage()
        print 'Nie zdefiniowałeś modułu'
        sys.exit(2)
    if not table:
        usage()
        print 'Nie zdefiniowałeś tabeli'
        sys.exit(2)

    model = args[0]                     # pierwszy argument nie będący opcję jest uznawany za nazwę modelu
    print 'Model: ' + model + ' zostanie stworzony w module: ' + module + ' pakietu: ' + package
    warning()
    moduleClass = Module(package, module)
    moduleClass.addModel(model, table)
    
if __name__ == '__main__':
    main(sys.argv[1:])
