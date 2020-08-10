MaryHadALittleLamb = song(time, melody, changes)
MaryHadALittleLamb_analysis_data = analysis_data(MaryHadALittleLamb)
note_index = MaryHadALittleLamb_analysis_data.index
column_names = MaryHadALittleLamb_analysis_data.columns

U,S,V = np.linalg.svd(MaryHadALittleLamb_analysis_data)

row_components = pd.DataFrame(U,index=note_index)
eigenvalues = pd.DataFrame(S)
col_components = pd.DataFrame(V,columns=column_names)

approx = np.matrix(U[:, :5]) * np.diag(S[:5]) * np.matrix(V[:5, :])
approx = np.around(np.absolute(approx),0)
approx_song = pd.DataFrame(approx,index=note_index,columns=column_names)

approx_song[['melody_note'+str(i) for i in range(1,13)]]
approx_song[['chord_note'+str(i) for i in range(1,13)]]

