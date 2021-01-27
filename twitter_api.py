a
    ��_�  �                   @   sH   d Z ddlZddlmZ ddlT ddlmZ dd� ZG dd	� d	e�ZdS )
zidistutils.command.bdist

Implements the Distutils 'bdist' command (create a built [binary]
distribution).�    N)�Command)�*)�get_platformc                  C   sP   ddl m}  g }tjD ]"}|�d| dtj| d f� q| |�}|�d� dS )zFPrint list of available formats (arguments to "--format" option).
    r   )�FancyGetopt�formats=N�   z'List of available distribution formats:)�distutils.fancy_getoptr   �bdist�format_commands�append�format_command�
print_help)r   �formats�formatZpretty_printer� r   �dC:\Users\rafae\AppData\Local\Temp\pip-unpacked-wheel-yl4k1dy6\setuptools\_distutils\command\bdist.py�show_formats   s    
�r   c                
   @   s�   e Zd ZdZdddde�  fdddd	d
gZdgZdddefgZdZ	ddd�Z
g d�Zdddddddddd�	Zdd� Zdd � Zd!d"� ZdS )#r	   z$create a built (binary) distribution)zbdist-base=�bz4temporary directory for creating built distributionsz
plat-name=�pz;platform name to embed in generated filenames (default: %s))r   Nz/formats for distribution (comma-separated list))z	dist-dir=�dz=directory to put final built distributions in [default: dist])�
skip-buildNz2skip rebuilding everything (for testing/debugging))zowner=�uz@Owner name used when creating a tar file [default: current user])zgroup=�gzAGroup name used when creating a tar file [default: current group]r   zhelp-formatsNz$lists available distribution formats)�	bdist_rpm�gztar�zip)�posix�nt)	Zrpmr   �bztar�xztar�ztar�tarZwininstr   Zmsi)r   zRPM distribution)�
bdist_dumbzgzip'ed tar file)r"   zbzip2'ed tar file)r"   zxz'ed tar file)r"   zcompressed tar file)r"   ztar file)�bdist_wininstzWindows executable installer)r"   zZIP file)Z	bdist_msizMicrosoft Installerc                 C   s.   d | _ d | _d | _d | _d| _d | _d | _d S )Nr   )�
bdist_base�	plat_namer   �dist_dir�
skip_build�group�owner)�selfr   r   r   �initialize_optionsQ   s    zbdist.initialize_optionsc                 C   s�   | j d u r(| jrt� | _ n|