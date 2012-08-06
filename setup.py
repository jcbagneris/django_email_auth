from distutils.core import setup

version = __import__('email_auth').VERSION

setup(
        name='django_email_auth',
        version=version,
        author='Jean-Charles Bagneris',
        author_email='jcbagneris@gmail.com',
        description='Yet another email auth system for the Django web framework',
        url="http://github.com/jcbagneris/django_email_auth",
        packages=['email_auth',],
        include_package_data=True,
        license='BSD',
        long_description=open('README.txt').read(),
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Web Environment",
            "Framework :: Django",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 2",
        ],
)

