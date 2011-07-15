#! /bin/bash
# Skrypt tworzący moduł podanej nazwie razem z zestawem katalogów i plików
# konfiguracyjnych

if [ "$#" -ne 2 ]
then
    echo -e "Nie podałeś wystarczającej liczby parametrów"
    exit -1
fi

package_directory_name="app/code/local/"

# echo -e "Podaj nazwę pakietu"
# read package_name
package_name=$1
# echo -e "Podaj nazwę modułu"
# read module_name
module_name=$2
if [ -d "${package_directory_name}${package_name}" ]
then
    module_directory_name="${package_directory_name}${package_name}/${module_name}"
    if [ -d "$module_directory_name" ]
    then
	echo -e "Ten moduł już istnieje!"
	exit -1
    fi
    # tworzenie niezbędnych katalogów
    mkdir $module_directory_name
    mkdir "${module_directory_name}/Block"
    mkdir "${module_directory_name}/controllers"
    mkdir "${module_directory_name}/etc"
    mkdir "${module_directory_name}/Helper"
    mkdir "${module_directory_name}/Model"
    mkdir "${module_directory_name}/sql"

    # tworzenie pliku konfiguracyjnego (wraz z routingiem)
    read -d '' config_file << EOF
<config>    
    <modules>
        <${package_name}_${module_name}>
            <version>0.1.0</version>
        </${package_name}_${module_name}>
    </modules>
    <frontend>
      <routers>
        <${module_name,,}>
          <use>standard</use>
          <args>
      	    <module>${package_name}_${module_name}</module>
      	    <frontName>${module_name,,}</frontName>
          </args>
        </${module_name,,}>
      </routers>
    </frontend>
</config> 
EOF

    echo -e "$config_file" >> "${module_directory_name}/etc/config.xml"

    read -d '' config_file_etc << EOF
<config>    
    <modules>
        <${package_name}_${module_name}>
            <active>true</active>
            <codePool>local</codePool>
        </${package_name}_${module_name}>
    </modules>
</config> 
EOF

    echo -e "$config_file_etc" >> "app/etc/modules/${package_name}_${module_name}.xml"

    # stworzenie akcji index kontrolera
    read -d '' controller_file << EOF
<?php 

class ${package_name}_${module_name}_IndexController extends Mage_Core_Controller_Front_Action {
  public function indexAction() {
    echo 'Stworzono nowy kontroler!';
  }
}
EOF

    echo -e "$controller_file" >> "${module_directory_name}/controllers/IndexController.php"
    
else
    echo -e "Taki pakiet jeszcze nie został utworzony"
    echo -e "Jako zabezpieczenie przed niepotrzebnym tworzeniem nowych pakietów musisz go stworzyć samemu"
    exit -1
fi
echo -e "Moduł został utworzony"
./clear_cache.sh