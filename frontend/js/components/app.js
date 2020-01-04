//IMPORT EXTERNAL COMPONENTS================================================
import React, { Fragment, useContext, useState } from "react";
import NProgress from "react-nprogress";
import { Image, Sidebar } from "semantic-ui-react";
import { ToastContainer } from "react-toastify";

//IMPORT INTERNAL COMPONENTS================================================
import LoadableError from "components/util/loadable-error";
import Header from "./header";
import Body from "./body";
import CategoriesSidebar from "./categories-sidebar";

//IMPORT INTERNAL ASSETS====================================================
import intrologo from "img/intrologo.png";
import loadinglogo from "img/loading.gif";

//IMPORT CONTEXTS===========================================================
import { CartContext } from "contexts/cart-context";
import { CurrentUserContext } from "contexts/current-user-context";
import { SidebarContext } from "contexts/sidebar-context";

// IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

// STYLE CLASSES DEFINITION==================================================
const imageClass = css({
    "&&&&": {
        display: "block",
        margin: "0 auto"
    }
});

const sidebarClass = css({
    "&&&&": {
        backgroundColor: "rgba(250, 250, 250, 0.9)",
        WebkitBoxShadow: "inset 0 0 6px rgba(0,0,0,0.3);",
        scrollbarWidth: "thin"
    },

});

const visibleClass = css({
    "&&&&": {
        height: "100vh"
    }
});

const pusherClass = css({
    "&&&&": {
        minHeight: "100vh"
    }
});

//COMPONENT=================================================================
function App() {
    NProgress.configure({ showSpinner: false });

    const { initializingCart } = useContext(CartContext)
    const { initializingUser } = useContext(CurrentUserContext)
    const { visible, hideSidebar } = useContext(SidebarContext)

    function renderIntro() {
        return (            
            <Fragment>
                <ToastContainer />
                <Image src={intrologo} alt=" " className={imageClass} />
                <Image src={loadinglogo} alt=" " className={imageClass} />
            </Fragment>
        )
    }

    function render() {
        if(initializingCart || initializingUser) {
            return renderIntro()
        }
        else{
            return (
                <Fragment>
                    <ToastContainer />
                    <LoadableError>
                        <Sidebar.Pushable>
                            <Sidebar
                                className={sidebarClass}
                                animation="overlay"
                                direction="left"
                                icon="labeled"
                                visible={visible}
                                width="wide"
                                onHide={hideSidebar}
                            >
                                <CategoriesSidebar />
                            </Sidebar>
                            <Sidebar.Pusher
                                className={(visible) ? visibleClass : pusherClass}
                                dimmed={visible}
                            > 
                                <Header />
                                <Body />
                            </Sidebar.Pusher>
                        </Sidebar.Pushable>
                    </LoadableError>
                </Fragment>
            )
        }
    }

    return render()    
}

//EXPORT COMPONENT==========================================================
export default App;