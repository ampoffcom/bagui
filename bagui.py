#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
bagui is an easygui wrapper for bagit.py
(https://github.com/edsu/bagit)
lang = de
"""
__author__ = 'steffen fritz'
__date__ = '04032014'
__version__ = '0.3b'
__contact__ = 'fritz@dla-marbach.de'
__description__ = "an easygui wrapper for bagit.py"

import sys
import os
import ConfigParser
import externals.easygui as easygui
import externals.bagit as bagit
import tarfile


def menu(title):
    """
    main menu
    """
    msg = "Auswahl"
    choices = ["Bag erstellen", "Bag validieren", "Hilfe", "Beenden"]
    choice = easygui.buttonbox(msg, title, choices)

    return choice


def create_config_file(title):
    """
    create config file. std dir and metadata
    """
    msg = "Der folgende Dialog führt durch die Erstellung einer Konfigurationsdatei."
    easygui.msgbox(msg)
    msg = "Im folgenden Dialog das Standard-Quellverzeichnis wählen"
    easygui.msgbox(msg)
    msg = "Standard-Quellverzeichnis waehlen"
    source_dir = easygui.diropenbox(msg, title)

    msg = "Bitte Standardwerte eingeben"
    msg = "Optionale Metadaten für bag-info.txt"
    fields = ["Erstellende Organisation", "Adresse Organisation",
              "Kontakt Name", "Kontakt Email"]

    orga, address, contact_name, contact_email = easygui.multenterbox(msg, title, fields)

    orga = orga.encode("utf-8")
    address = address.encode("utf-8")
    contact_name = contact_name.encode("utf-8")
    contact_email = contact_email.encode("utf-8")

    fd = open("config.cfg", "w")
    fd.write("[DEFAULTS]\n")
    fd.write("Orga = " + orga + "\n")
    fd.write("Address = " + address + "\n")
    fd.write("Contact_name = " + contact_name + "\n")
    fd.write("Contact_email = " + contact_email + "\n")
    fd.write("Source_dir = " + source_dir + "\n")

    fd.close()


def read_config_file():
    """
    read config file and return default settings
    """
    config = ConfigParser.RawConfigParser()
    config.read("config.cfg")

    orga = config.get("DEFAULTS", "Orga")
    address = config.get("DEFAULTS", "Address")
    contact_name = config.get("DEFAULTS", "Contact_name")
    contact_email = config.get("DEFAULTS", "Contact_email")
    source_dir = config.get("DEFAULTS", "Source_dir")

    return orga, address, contact_name, contact_email, source_dir


def metadata(title, orga, address, contact_name, contact_mail):
    """
    optional metadata for bag-info.txt
    """
    msg = "Optionale Metadaten für bag-info.txt"
    fields = ["Erstellende Organisation", "Adresse Organisation",
              "Kontakt Name", "Kontakt Email"]
    
    fieldValues = [orga, address, contact_name, contact_mail]
    
    orga, address, contact_name, contact_email = easygui.multenterbox(msg, title, fields, fieldValues)

    orga = orga.encode("utf-8")
    address = address.encode("utf-8")
    contact_name = contact_name.encode("utf-8")
    contact_email = contact_email.encode("utf-8")

    return orga, address, contact_name, contact_email


def create_bag(title, orga, address, contact_name, contact_mail, default_source_dir):
    """
    create bag from directory
    """
    msg = "Quellverzeichnis waehlen"
    source_dir = easygui.diropenbox(msg, title,default=default_source_dir)
    base_name = os.path.basename(source_dir)
    orga, address, contact_name, contact_email = metadata(title, orga, address, contact_name, contact_mail)

    try:
        bagit.make_bag(source_dir, {'Source_Organization': orga,
                                    'Organization-Address': address,
                                    'Contact-Name': contact_name,
                                    'Contact-Email': contact_email})

        easygui.msgbox(msg="Bag erfolgreich erstellt")
        msg = "Soll die Bag mit tar zu einer Datei zusammengefasst werden?"
        choices = ["Ja", "Nein"]
        choice = easygui.buttonbox(msg, title, choices)

        if choice == "Ja":
            try:
                tar = tarfile.open(source_dir + ".tar", "w")
                tar.add(source_dir, base_name)
                tar.close()

                msg = "Archivdatei " + base_name + ".tar wurde erfolgreich in " + source_dir + \
                      " erstellt."

                easygui.msgbox(msg, title)

            except RuntimeError, err:
                msg = "Bei der Verarbeitung mit tar trat ein Fehler auf." \
                      " Programm wird beendet."

                easygui.msgbox(msg, title)
                print(str(err))
                sys.exit(1)
        else:
            easygui.msgbox(msg="Bag erfolgreich in " +
                            source_dir +
                            " erstellt.")

    except RuntimeError, err:
        print(str(err))
        print("Beim Erstellen des Bags trat ein Fehler auf. "
              "Programm wird beendet.")
        sys.exit(1)


def validate_bag(title, source_dir):
    """
    validate bag
    """
    msg = "Bag wählen"
    source_bag = easygui.diropenbox(msg, title, default=source_dir)

    try:
        bag = bagit.Bag(source_bag)
    except IOError, err:
        msg = "Es trat ein Fehler auf. " + str(err)
        easygui.msgbox(msg, title)
        sys.exit(1)

    try:
        bag.validate()
        msg = "Bag ist valide."
        easygui.msgbox(msg, title)

    except bagit.BagValidationError, err:
        msg = str(err)
        easygui.msgbox(msg, title)


def helpmsg(title):
    """
    show usage
    this one needs more text
    """
    msg = "Noch nicht implementiert"
    easygui.msgbox(msg, title)


def warning(title):
    """
    warning message at startup
    """
    msg = "Achtung! Nur auf Kopien arbeiten! BagIt ändert die " \
          "Verzeichnisstruktur des Quellverzeichnisses!"

    easygui.msgbox(msg, title)


def main():
    """
    the main function
    """
    title = "Bagui - v.0.3b"
    easygui.msgbox(msg=title)
    warning(title)

    if os.path.exists("config.cfg"):
        orga, address, contact_name, contact_email, source_dir = read_config_file()
    
    else:
        create_config_file(title)
        orga, address, contact_name, contact_email, source_dir = read_config_file()

    while True:
        choice = menu(title)
        if choice == "Bag erstellen":
            create_bag(title, orga, address, contact_name, contact_email, source_dir)
        elif choice == "Bag validieren":
            validate_bag(title, source_dir)
        elif choice == "Hilfe":
            helpmsg(title)
        else:
            sys.exit(0)

if __name__ == '__main__':
    main()
