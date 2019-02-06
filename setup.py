from setuptools import setup, find_packages

setup(
    name='probcause',
    version='1.0',
    packages=[  # Names of packages
        'probcause.client_side',
        'probcause.server_side',
        'probcause.demos',
        'probcause.tests',
        'probcause.util',
    ],
    package_dir={  # File paths
        'probcause.client_side': 'client_side',
        'probcause.server_side': 'server_side',
        'probcause.demos': 'demos',
        'probcause.tests': 'tests',
        'probcause.util': 'util',
    },
    package_data={  # Data
        'probcause.tests': [
            'wc_forecasts.csv'
        ],
    },
)
