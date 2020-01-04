//IMPORT EXTERNAL COMPONENTS================================================
import React, { useState } from "react";
import { Responsive, Grid } from "semantic-ui-react";

//COMPONENT=================================================================
function ResponsiveGrid({ children, className, widescreen, largescreen, computer, tablet, mobile=1, ...others }) {
    const [colNum, setColNum] = useState(1);

    function onWidthUpdate() {
        if(widescreen !== undefined && window.innerWidth >= Responsive.onlyWidescreen.minWidth){
            setColNum(widescreen);
        }
        else if(largescreen !== undefined && window.innerWidth >= Responsive.onlyLargeScreen.minWidth){
            setColNum(largescreen);
        }
        else if(computer !== undefined && window.innerWidth >= Responsive.onlyComputer.minWidth){
            setColNum(computer);
        }
        else if(tablet !== undefined && window.innerWidth >= Responsive.onlyTablet.minWidth){
            setColNum(tablet);
        }
        else{
            setColNum(mobile);
        }
    }

    return (
        <Responsive
            as={Grid}
            onUpdate={onWidthUpdate}
            columns={colNum}
            className={className}
            fireOnMount
            {...others}
        >
            {children}
        </Responsive>
    )
}

//EXPORT COMPONENT==========================================================
export default ResponsiveGrid;