//IMPORT EXTERNAL COMPONENTS================================================
import { useEffect, useReducer } from "react";
import NProgress from "react-nprogress";

//IMPORT EXTERNAL FUNCTIONS=================================================
import axios from "axios";
import { cloneDeep } from "lodash";

//HOOK======================================================================
function useRequestData(request, afterRequest) {
    const initialState = {
        loading: true,
        progress: 0,
        status: 0,
        headers: null,
        data: null,
        error: null
    }

    function reducer(state, action) {
        switch (action.type) {
            case "REQUEST_START":
                return {
                    ...state,
                    loading: true,
                    progress: 0
                }
            case "UPLOAD_PROGRESS":
                return {
                    ...state,
                    progress: action.progress
                }
            case "RECEIVE_DATA":
                NProgress.done();
                return {
                    ...state,
                    loading: false,
                    status: action.status,
                    headers: action.headers,
                    data: action.data,
                    error: null
                }
            case "RECEIVE_ERROR":
                NProgress.done();
                return {
                    ...state,
                    loading: false,
                    status: action.status,
                    headers: null,
                    data: null,
                    error: action.error
                }
            default:
                return state;
        }
    }

    var executeCancel = () => {};

    const [state, dispatch] = useReducer(reducer, initialState);

    useEffect(() => {
        if (request !== null) {
            dispatch({type: "REQUEST_START"});
            NProgress.set(0.0)
            NProgress.start();

            let clean_request = cloneDeep(request);
            for (var key in clean_request.data) {
                if (["", null].includes(clean_request.data[key])){
                    delete clean_request.data[key]
                }
            }

            axios(
                {
                    ...clean_request,
                    cancelToken: new axios.CancelToken((c) => executeCancel = c),
                    onUploadProgress: (e) => {
                        dispatch({type: "UPLOAD_PROGRESS", progress: Math.round((e.loaded * 100) / e.total)});
                    }
                }
            ).then(
                (response) => {
                    dispatch({type: "RECEIVE_DATA", ...response})
                }
            ).catch(
                (error) => {
                    if(axios.isCancel(error)){
                        //pass
                    }
                    else if(error.response){
                        if(error.response.status === 401){
                            window.location.replace("/login");
                        }
                        else{
                            dispatch({type: "RECEIVE_ERROR", status: error.response.status, error: error.response.data})
                        }
                    }
                    else if(error.request){
                        dispatch({type: "RECEIVE_ERROR", status: 600, error: "No Internet connection available."})
                    }
                    else{
                        dispatch({type: "RECEIVE_ERROR", status: 601, error: "Internal error."})
                    }
                }
            ).then(
                () => {
                    if(typeof(afterRequest) !== "undefined"){
                        for (var key in afterRequest) {
                            if (typeof(afterRequest[key]) === "function"){
                                afterRequest[key]()
                            }
                        }
                    }
                }
            )
        }

        return () => {
            NProgress.done();
            if(request !== null){
                executeCancel();
            }
        }
    }, [request])

    return state;
}

//EXPORT HOOK===============================================================
export default useRequestData;