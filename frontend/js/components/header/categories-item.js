//IMPORT EXTERNAL COMPONENTS================================================
import React, { useContext, useState, useEffect } from "react";
import { Menu, Icon, Transition } from "semantic-ui-react";

//IMPORT CONTEXTS===========================================================
import { SidebarContext } from "contexts/sidebar-context";

//IMPORT HOOKS==============================================================
import useDidMount from "hooks/did-mount";

// //IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

// //STYLE CLASSES DEFINITION==================================================
const itemClass = css({
    "&&&&:hover": {
        backgroundColor: "deepskyblue"
    }
})

const exclamationClass = css({
    "&&&&": {
        position: "absolute",
        right: "1px"
    }
})

//COMPONENT=================================================================
function CategoriesItem() {
    const { visible, sidesessions, sidebrands, sidekinds, showSidebar } = useContext(SidebarContext);
    const [visibleNotification, setVisibleNotification] = useState(false);
    const didMount = useDidMount();

    useEffect(() => {
        if(!didMount && visibleNotification === true){
            setVisibleNotification(false);
        }
    }, [visible])

    useEffect(() => {
        if(!didMount){
            if(sidesessions.length > 0 || sidebrands.length > 0 || sidekinds.length > 0){
                setVisibleNotification(true);
                setTimeout(() => setVisibleNotification(false), 5000);
            }
        }
    }, [sidesessions, sidebrands, sidekinds])

    return (
        <Menu.Item
            icon
            className={itemClass}
            onClick={showSidebar}
        >
            <Icon name="indent" size="big" />
            <Transition
                animation="drop"
                duration={500}
                visible={visibleNotification}
            >
                <Icon className={exclamationClass} corner="top right" name="info circle" color="orange" />
            </Transition>
        </Menu.Item>
    )
}

//EXPORT COMPONENT==========================================================
export default CategoriesItem;