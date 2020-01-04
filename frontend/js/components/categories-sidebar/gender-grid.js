//IMPORT EXTERNAL COMPONENTS================================================
import React, { Fragment, useContext } from "react";
import { Link } from "react-router-dom";
import { Grid, Header, Icon, Label } from "semantic-ui-react";

//IMPORT CONTEXTS===========================================================
import { SidebarContext } from "contexts/sidebar-context";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const headerRowClass = css({
    "&&&&": {
        backgroundColor: "rgba(250, 250, 250, 0.9)"
    }
})

const headerClass = css({
    "&&&&": {
        marginBottom: "0"
    }
})

const pointerClass = css({
    "&&&&:hover": {
        cursor: "pointer"
    }
})

const itemRowClass = css({
    "&&&&": {
        boxShadow: "none",
        MozBoxShadow: "none",
        WebkitBoxShadow: "none"
    }
})

const itemClass = css({
    "&&&&&": {
        color: "black",
        backgroundColor: "lightskyblue",
        boxShadow: "none",
        MozBoxShadow: "none",
        WebkitBoxShadow: "none",
        border: "1px solid rgba(212, 212, 213, 0.8)",
        
    },
    "&&&&:hover": {
        backgroundColor: "deepskyblue"
    }
})

//COMPONENT=================================================================
function GenderGrid() {
    const { hideSidebar } = useContext(SidebarContext)

    return (
        <Fragment>
            <Grid.Row className={headerRowClass} columns={1}>
                <Grid.Column>
                    <Header as="h3" className={headerClass}>Gender</Header>
                    <Label corner="right" className={pointerClass} onClick={hideSidebar}>
                        <Icon name="x" fitted className={pointerClass} />
                    </Label>
                </Grid.Column>
            </Grid.Row>
            <Grid.Row columns={2} className={itemRowClass}>
                <Grid.Column 
                    className={itemClass}
                    as={Link}
                    to="/outlet/men"
                    onClick={hideSidebar}
                >
                    <Icon name="male" />Men
                </Grid.Column>
                <Grid.Column 
                    className={itemClass}
                    as={Link}
                    to="/outlet/women"
                    onClick={hideSidebar}
                >
                    <Icon name="female" />Women
                </Grid.Column>
            </Grid.Row>
        </Fragment>
    )
}

//EXPORT COMPONENT==========================================================
export default GenderGrid;