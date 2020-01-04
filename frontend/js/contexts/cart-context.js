//IMPORT EXTERNAL COMPONENTS================================================
import React, { createContext, useReducer, useState, useEffect } from "react";

//IMPORT INTERNAL FUNCTIONS=================================================
import toastMessage from "lib/toast-message";

//IMPORT HOOKS==============================================================
import useRequestData from "hooks/request-data";
import useDidMount from "hooks/did-mount";

//CONTEXT===================================================================
export const CartContext = createContext();

function CartContextProvider(props) {
    const { children } = props;

    const initialState = {
        initializingCart: true,
        updatingCart: false,
        products: [],
        productsType: 0,
        itemCount: -1,
        total: {},
        loadCart: loadCart,
        updateCartItem: updateCartItem,
        removeCartItem: removeCartItem,
        startOrder: startOrder
    }

    function reducer(state, action) {
        switch (action.type) {
            case "START_UPDATE":
                return {
                    ...state,
                    updatingCart: true
                }
            case "FINISH_UPDATE":
                return {
                    ...state,
                    updatingCart: false
                }
            case "RECEIVE_DATA":
                return {
                    ...state,
                    initializingCart: false,
                    products: action.products,
                    productsType: action.products.length,
                    itemCount: getItemsCount(action.products),
                    total: action.total
                }
            default:
                return state;
        }
    }

    const [state, dispatch] = useReducer(reducer, initialState);
    const didMount = useDidMount();
    const [request, setRequest] = useState(null);
    const requestData = useRequestData(request);

    useEffect(() => {
        const { status, data } = requestData;
        if(status === 204){
            dispatch({type: "RECEIVE_DATA", products: [], total: {outlet: 0.0, retail: 0.0, symbol: "£"}});
        }
        else if(status === 200){
            const { products, total } = data;
            dispatch({type: "RECEIVE_DATA", products: products, total: total});
        }
        else if(status >= 400){
            const { error } = requestData;
            if (status === 400) {
                loadCart()
            }
            else if(status === 600){
                toastMessage("error", { message: error.error, submessage: "Check your connection and refresh."})
            }
            else{
                toastMessage("error", { message: error.error, submessage: "Please refresh the page."})
            }
        }
    }, [requestData])

    useEffect(() => {
        loadCart()
    }, [])

    useEffect(() => {
        if(!didMount){
            dispatch({type: "FINISH_UPDATE"});
        }
    }, [state.itemCount])

    function getItemsCount(products) {
        let count = 0;
        products.forEach((p) => {
            count += p.amount; 
        })
        
        return count;
    }

    function loadCart() {
        dispatch({type: "START_UPDATE"});
        setRequest({
            url: "/api/cart",
            method: "get",
            responseType: "json"
        })
    }

    function updateCartItem(itemid, amount) {
        dispatch({type: "START_UPDATE"});
        setRequest({
            url: `/api/cart/update/${itemid}/${amount}`,
            method: "post",
            responseType: "json"
        })
    }

    function removeCartItem(itemid) {
        dispatch({type: "START_UPDATE"});
        setRequest({
            url: `/api/cart/remove/${itemid}`,
            method: "post",
            responseType: "json"
        })
    }

    function startOrder() {
        dispatch({type: "START_UPDATE"});
    }

    return (
        <CartContext.Provider value={{...state}}>
            {children}
        </CartContext.Provider>
    )
}

//EXPORT HOOK===============================================================
export default CartContextProvider;