#! /bin/bash
# Skrypt usuwający moduł podanej nazwie razem z zestawem katalogów i plików
# konfiguracyjnych
package_directory_name="app/code/local/"

if [ "$#" -ne 2 ]
then
    echo -e "Nie podałeś wystarczającej liczby parametrów"
    exit -1
fi

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
	rm -rf $module_directory_name
	rm "app/etc/modules/${package_name}_${module_name}.xml"
    else
	echo -e "Podany moduł nie istnieje"
    fi
else
    echo -e "Tego pakietu jeszcze nie ma, w związku z czym niemożliwe jest usunięcie z niego pakietu"
    exit -1
fi
echo -e "Moduł został usunięty"
./clear_cache.sh