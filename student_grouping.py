try:
    from enum import Enum
    from io import BytesIO, StringIO
    from typing import Union
    from sklearn.cluster import KMeans

    import pandas as pd
    import matplotlib.pyplot as plt
    import streamlit as st
    import time
except Exception as e:
    print(e)


def main():
    """Run this function to display the Streamlit app"""
    st.title('Group Formation Tool')
    # st.info(__doc__)
    # st.markdown(STYLE, unsafe_allow_html=True)
    st.set_option('deprecation.showfileUploaderEncoding', False)
    file = st.file_uploader("Upload file", type=["xlsx"])
    show_file = st.empty()

    if not file:
        show_file.info("Please upload only file type: " + ", ".join(["xlsx"]))
        return
 
    content = file.getvalue()

    if (file):
        data = pd.read_excel(file)
        st.dataframe(data.head(50))

        def bfi_preprocess(x):
            bfi_list = x.split(' ')
            bfi_A, bfi_C, bfi_E, bfi_O, bfi_N = 0,0,0,0,0
            if "A" in bfi_list:
                bfi_A = 1
            
            if "C" in bfi_list:
                bfi_C = 1
            
            if "E" in bfi_list:
                bfi_E = 1
                
            if "O" in bfi_list:
                bfi_O = 1
            
            if "N" in bfi_list:
                bfi_N = 1
            
            return pd.Series([bfi_A, bfi_C, bfi_E, bfi_O, bfi_N])

        def vark_preprocess(x):
            vark_list = x.split(' ')
            vark_V, vark_A, vark_R, vark_K = 0,0,0,0
            if "V" in vark_list:
                vark_V = 1
            
            if "A" in vark_list:
                vark_A = 1
            
            if "R" in vark_list:
                vark_R = 1
                
            if "K" in vark_list:
                vark_K = 1
            
            return pd.Series([vark_V, vark_A, vark_R, vark_K])


        data[["BFI_A", "BFI_C", 
            "BFI_E", "BFI_O", 
            "BFI_N"]] = data["BFI  Dominant"].apply(bfi_preprocess)

        data[["VARK_V", "VARK_A", 
            "VARK_R", "VARK_K"]] = data["VARK Dominant"].apply(vark_preprocess)
        data.head(20)


        X = data[["BFI_A", "BFI_C", 
            "BFI_E", "BFI_O", 
            "BFI_N", "VARK_V", "VARK_A", 
            "VARK_R", "VARK_K"]].values


        kmeans = KMeans(n_clusters=5)
        kmeans.fit(X)
        y_kmeans = kmeans.predict(X)


        # get_ipython().system('pip install matplotlib -q')

        import matplotlib.pyplot as plt

        plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')

        centers = kmeans.cluster_centers_
        plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
        data["output_group"] = y_kmeans

        with st.spinner('Wait for it...'):
            time.sleep(2)
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.1)
        my_bar.progress(percent_complete + 1)

        st.dataframe(data.head(50))

        data.groupby('output_group').agg(['count'])["Student ID"].plot.bar();
        data.to_excel(r'Result.xlsx', index = False)
        st.success('Done! Students has been grouped and file has been exported')


    file.close()

main()