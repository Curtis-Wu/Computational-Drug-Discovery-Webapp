import numpy as np
import pickle
import os
import pandas as pd
from chembl_webresource_client.new_client import new_client
import subprocess
from padelpy import padeldescriptor


if __name__ == "__main__":
    my_str = "CHEMBL133897 CHEMBL336398"
    my_list = list(my_str.split(' '))
    #print(my_list)
    #my_array = np.array([my_list])
    #model = pickle.load(open("data/trained_model.pkl"),"rb")
    molecule = new_client.molecule
    selection = ['canonical_smiles','molecule_chembl_id']
    my_res = []
    mols = molecule.filter(molecule_chembl_id__in=my_list).only(['molecule_chembl_id', 'molecule_structures'])
    for molecule in mols:
        my_res.append([molecule['molecule_structures']['canonical_smiles'],molecule['molecule_chembl_id']])
    df = pd.DataFrame(my_res)
    df.to_csv('models/acetylcholinesterase/molecule.smi', sep='\t', index=False, header=False)
    #process = subprocess.run('padel.sh', shell=True, check=True, timeout=10) 

    fp = pickle.load(open('models/padel_py/padel.pkl','rb'))
    fingerprint = 'Substructure'
    fingerprint_output_file = ''.join([fingerprint,'.csv']) #Substructure.csv
    fingerprint_descriptortypes = fp[fingerprint]

    padeldescriptor(mol_dir='molecule.smi', 
                    d_file=fingerprint_output_file, #'Substructure.csv'
                    #descriptortypes='SubstructureFingerprint.xml', 
                    descriptortypes= fingerprint_descriptortypes,
                    detectaromaticity=True,
                    standardizenitro=True,
                    standardizetautomers=True,
                    threads=2,
                    removesalt=True,
                    log=True,
                    fingerprints=True)


    