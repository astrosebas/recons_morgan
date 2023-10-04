# Select sepctra with OBJECT id from RKSTAR Masterlist
def RKS_spec(dataset_root,out_name):
    
    ## Public reduced data
    pub_data = 'ftp/pub/SMARTS'
    masterlist = pd.read_csv(sample+'RKScatalog50pc_all.csv')
    #masterlist = pd.read_csv(sample+'tsn50_chiron_gdr3.csv')

    # All datasets YYMMDD
    print('dataset_root 2', dataset_root)
    datasets = [dI for dI in os.listdir(dataset_root) if \
                os.path.isdir(os.path.join(dataset_root,dI))]
    datasets.sort()
    datasets.remove('fifteen_twenty_pc')
    datasets.remove('ten_fifteen_pc')
    datasets.remove('ten_test')
    datasets.remove('test')
    datasets.remove('twenty_five_pc')
    log.info('Datasets retrieved')

    """
    # Datasets by year taken
    data2017 = list(filter(lambda x:x.startswith(("17")), datasets)) 
    data2018 = list(filter(lambda x:x.startswith(("18")), datasets)) 
    data2019 = list(filter(lambda x:x.startswith(("19")), datasets)) 
    data2020 = list(filter(lambda x:x.startswith(("20")), datasets)) 
    data2021 = list(filter(lambda x:x.startswith(("21")), datasets)) 
    data2022 = list(filter(lambda x:x.startswith(("22")), datasets)) 
    data2023 = list(filter(lambda x:x.startswith(("23")), datasets)) 

    data_years = [data2017, data2018, data2019,data2020]#,
    #             data2021,data2022,data2023]
    #data_years = [data2021,data2022,data2023]
    """
    
    # Creates a list with the paths to the spectra files.    
    calib = ['ThAr','quartz','iodine']
    data = []

    year = 2017 # 2021
    for year_list in data_years:

        log.info(f'========================= DATASETS YEAR {year} =========================')
        for dataset in year_list:

            path_dataset = []
            #if dataset == '170624':
            filename = (pathlib.Path(dataset_root) / dataset).glob("*.fits")
            path_dataset.extend(filename)
            path_dataset = list(filter(None, path_dataset))

            for path in path_dataset:

                #path_ = str(path)
                #path_strings = path_.split("/")
                #datadate = path_strings[7] #dataset date

                # Opening FITS and getting header
                fits_info = fits.open(path)
                hdu = fits_info['PRIMARY'].header

                # Check for keywords existence
                if 'OBJECT' in hdu:  

                    # Getting object name
                    ob_name = hdu['OBJECT']
                    
                    if ob_name not in calib:
                        
                        row = masterlist.loc[(masterlist['RKS'] == ob_name)|\
                                                    (masterlist['HIP'] == ob_name)|\
                                                    (masterlist['G2K'] == ob_name)]#,\
                                                    #("ra_edr3","dec_edr3","pmra","pmdec","parallax")].iloc[0]
            
                        # if not row.empty():
                        if len(row.index) != 0:
                            #do something  

                            #OBJECT = []
                            #EXPTIME = []
                            #DATE = []
                            #PATH = []
                            #EMAVG = []

                            path_ = str(path)
                            path_strings = path_.split("/")
                            datadate = path_strings[7] #dataset date

                            # Calculating SN for all the spectrum
                            # from Paredes et al. 2021
                            if 'EMAVG' in hdu:
                                em_avg = hdu['EMAVG']
                                snr_em = SNR_em(path)
                                snr_em = np.round(snr_em,3)
                            else:
                                em_avg = 0.0
                                snr_em = 0.0
                            
                            prop_id = hdu['PROPID']
                            ra = hdu['RA']
                            dec = hdu['DEC']
                            epoch = hdu['EPOCH']
                            time = hdu['UTSHUT']
                            decker = hdu['DECKER']
                            exptime = hdu['EXPTIME']
                            exptime = hdu['EXPTIME']
                            
                            #OBJECT.append(ob_name)
                            #PATH.append(path)
                            
                            
                            rks_info =  [ob_name,prop_id,ra,dec,epoch,time,decker,\
                                         exptime,em_avg,snr_em,path]
                            #rks_info =  [ob_name,exptime,em_avg,snr_em,date,path]
                            data.append(rks_info)
                        # else:
                        #    log.warn(f'No RKS in dataset {datadate}')
                        
            log.info(f'RKS in dataset {datadate} retrieved')
            print('=======================================================')
        
        columns_cat = ["OBJECT", "PROPID", "RA", "DEC", "EPOCH", "UTSHUT", "DECKER",\
                        "EXPTIME", "EMAVG", "SN_EMAVG", "PATH"]
        rks_paths = pd.DataFrame(data, columns=columns_cat)
        # ["OBJECT","EXPTIME","EMAVG","SNREM","DATE", "PATH"]
        rks_paths.to_csv(out_name+str(year)+'_v2.csv',index=False)
        year += 1
        log.info('Spectra list done')