from logging import error
from pydub import AudioSegment
from pydub.silence import split_on_silence
import glob
import os.path
from feature_extraction import Feature_Extraction
import pandas as pd


# Split the wav files into chunks

# loop thru the folders
#folder_path = r"dataset\ReadText\HC\*.wav"
f = Feature_Extraction()
def split_into_chunks():
    folder_paths = [r"dataset\ReadText\HC\*.wav", r"dataset\ReadText\PD\*.wav"]
    parent_dirs = [r"dataset\MDVR\HC", r"dataset\MDVR\PD"]

    for i in range(len(folder_paths)):
        for file in glob.glob(folder_paths[i]):
            try:
                print(file)
                #split to get HC\ID00
                path2, filename2 = os.path.split(file)
                root, ext = os.path.splitext(filename2)
                x = root.split('_')[0]

                directory = x
                parent_dir = parent_dirs[i] #r"dataset\MDVR\HC"

                path = os.path.join(parent_dir, directory)
                print(path)
                os.makedirs(path)

                filename = file
                sound_file = AudioSegment.from_wav(filename)
                audio_chunks = split_on_silence(sound_file, 
                    # must be silent for at least half a second
                    min_silence_len=1000,
                    # consider it silent if quieter than -16 dBFS
                    silence_thresh=-40)
                for j, chunk in enumerate(audio_chunks):
                    out_file = path + "/chunk{0}.wav".format(j)
                    print ("exporting", out_file)
                    chunk.export(out_file, format="wav")
            except Exception as e:
                print(e)
                print("error while handling file: ", file)


def extract_features_from_chunks(folder_path, label):
   
    #folder_path = r"dataset\MDVR\HC"
    df_all = []
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            folder_path = os.path.join(root, dir)
            folder_path = r'%s' % folder_path + "\*.wav"
            print(folder_path)
            df_hc = f.extract_features_from_folder(folder_path)
            #print(df_hc)
            df_all.append(df_hc)
            #print(df_all_hc)
    # call the function to extract the features from the folder
    df_all = pd.concat(df_all)
    df_all['label'] = label
    return df_all


#run the splitting code
split_into_chunks()

#extract the features
hc = extract_features_from_chunks(r"dataset\MDVR\HC", 0)
pd_1 = extract_features_from_chunks(r"dataset\MDVR\PD", 1)
df_acoustic_features = pd.concat([hc,pd_1])
f.convert_to_csv(df_acoustic_features,"MDVR_acoustic_features_chunks")

    


   