//IMPORT EXTERNAL COMPONENTS================================================
import React, { useReducer, createContext } from "react";

// IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

// STYLE CLASSES DEFINITION==================================================
const disabledClass = css({
    "&&&&": {
        overflow: "hidden"
    }
});

//CONTEXT===================================================================
export const SidebarContext = createContext();

function SidebarContextProvider(props) {
    const { children } = props;

    const initialState = {
        visible: false,
        sidesessions: [],
        sidebrands: [],
        sidekinds: [],
        showSidebar: showSidebar,
        hideSidebar: hideSidebar,
        updateItems: updateItems
    }

    function reducer(state, action) {
        switch (action.type) {
            case "TOGGLE_VISIBLE":
                return {
                    ...state,
                    visible: action.visible
                }
            case "UPDATE":
                return {
                    ...state,
                    sidesessions: action.sidesessions,
                    sidebrands: action.sidebrands,
                    sidekinds: action.sidekinds,
                }
            default:
                return state;
        }
    }

    const [state, dispatch] = useReducer(reducer, initialState);

    function disableBody(e) {
        e.preventDefault();
    }

    function showSidebar() {
        window.scrollTo(0, 0);
        document.body.classList.add(disabledClass);
        document.body.ontouchstart = disableBody;
        dispatch({type: "TOGGLE_VISIBLE", visible: true})
    }

    function hideSidebar() {
        document.body.classList.remove(disabledClass);
        document.body.removeEventListener("touchstart", disableBody);
        dispatch({type: "TOGGLE_VISIBLE", visible: false})
    }

    function updateItems(sidesessions, sidebrands, sidekinds) {
        dispatch({type: "UPDATE", sidesessions, sidebrands, sidekinds});
    }

    return (
        <SidebarContext.Provider value={{...state}}>
            {children}
        </SidebarContext.Provider>
    )
}

//EXPORT HOOK===============================================================
export default SidebarContextProvider;