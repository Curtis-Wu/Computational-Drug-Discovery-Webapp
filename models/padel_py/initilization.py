import glob
import pickle
xml_files = glob.glob("models/padel_py/*")
xml_files.sort()
FP_list = ['AtomPairs2DCount',
 'AtomPairs2D',
 'EState',
 'CDKextended',
 'CDK',
 'CDKgraphonly',
 'KlekotaRothCount',
 'KlekotaRoth',
 'MACCS',
 'PubChem',
 'SubstructureCount',
 'Substructure']
fp = dict(zip(FP_list, xml_files))
pickle.dump(fp,open('models/padel_py/padel.pkl','wb'))


