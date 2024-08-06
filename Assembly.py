import sys
import os
import re
from dataclasses import dataclass
from typing import List, Dict

# General Information about an assembly is controlled through the following 
# set of attributes. Change these attribute values to modify the information
# associated with an assembly.
@dataclass
class AssemblyInfo:
    title: str = "BioRad.Example_Client"
    description: str = ""
    configuration: str = ""
    company: str = "Bio-Rad"
    product: str = "BioRad.Example_Client"
    copyright: str = "© 2014 Bio-Rad Laboratories. All Rights Reserved."
    trademark: str = ""
    culture: str = ""
    com_visible: bool = False
    guid: str = "149185e8-c631-4015-b591-35029ca62a66"
    version: str = "1.0.*"
    file_version: str = "1.0.0.0"

