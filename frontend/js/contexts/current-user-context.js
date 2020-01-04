//IMPORT EXTERNAL COMPONENTS================================================
import React, { useEffect, useReducer, createContext } from "react";

//IMPORT INTERNAL FUNCTIONS=================================================
import axios from "axios";

//IMPORT INTERNAL FUNCTIONS=================================================
import toastMessage from "lib/toast-message";

//CONTEXT===================================================================
export const CurrentUserContext = createContext();

function CurrentUserContextProvider(props) {
    const { children } = props;

    const initialState = {
        initializingUser: true,
        isLoggedIn: false,
        status: 0,
        data: null,
        error: null
    }

    function reducer(state, action) {
        switch (action.type) {
            case "RECEIVE_DATA":
                return {
                    ...state,
                    initializingUser: false,
                    isLoggedIn: action.isLoggedIn,
                    status: action.status,
                    data: action.data,
                    error: null
                }
            case "RECEIVE_ERROR":
                return {
                    ...state,
                    initializingUser: false,
                    isLoggedIn: false,
                    status: action.status,
                    data: null,
                    error: action.error
                }
            default:
                return state;
        }
    }

    const [state, dispatch] = useReducer(reducer, initialState);

    useEffect(() => {
        axios(
            {
                url: "/api/user/current",
                method: "get",
                responseType: "json"
            }
        ).then(
            (response) => {
                toastMessage("login", {...response.data})
                dispatch({type: "RECEIVE_DATA", isLoggedIn: true, ...response})
            }
        ).catch(
            (error) => {
                if(error.response){
                    if(error.response.status === 401){
                        dispatch({type: "RECEIVE_DATA", status: error.response.status, isLoggedIn: false, data: null})
                    }
                    else{
                        toastMessage("error", { message: error.response.data.error, submessage: "Please refresh the page."})
                        dispatch({type: "RECEIVE_ERROR", status: error.response.status, error: error.response.data})
                    }
                }
            }
        )
    }, [])

    return (
        <CurrentUserContext.Provider value={{...state}}>
            {children}
        </CurrentUserContext.Provider>
    )
}

//EXPORT HOOK===============================================================
export default CurrentUserContextProvider;