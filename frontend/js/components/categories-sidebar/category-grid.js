//IMPORT EXTERNAL COMPONENTS================================================
import React, { Fragment, useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import { Grid, Header, Label, Icon, Transition } from "semantic-ui-react";

//IMPORT CONTEXTS===========================================================
import { SidebarContext } from "contexts/sidebar-context";

//IMPORT HOOKS==============================================================
import useDidMount from "hooks/did-mount";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const headerRowClass = css({
    "&&&&": {
        backgroundColor: "rgba(250, 250, 250, 0.9)",
        boxShadow: "none",
        MozBoxShadow: "none",
        WebkitBoxShadow: "none",
        cursor: "pointer"
    }
})

const itemRowClass = css({
    "&&&&": {
        boxShadow: "none",
        MozBoxShadow: "none",
        WebkitBoxShadow: "none",
        display: "flex !important"
    }
})

const itemClass = css({
    "&&&&&": {
        color: "black",
        backgroundColor: "lightskyblue",
        padding: "0.5em",
        display: "flex",
        flexGrow: 1,
        alignItems: "center",
        justifyContent: "center",
        boxShadow: "none",
        MozBoxShadow: "none",
        WebkitBoxShadow: "none",
        border: "1px solid rgba(212, 212, 213, 0.8)",
    },
    "&&&&&:hover": {
        backgroundColor: "deepskyblue"
    }
})

const centerClass = css({
    "&&&&": {
        float: "left",
        marginRight: "0",
        opacity: "0"
    }
})

const caretClass = css({
    "&&&&": {
        float: "right",
        marginRight: "0"
    }
})

const labelClass = css({
    "&&&&": {
        padding: "0.25em",
        paddingTop: "0.15em",
        marginLeft: "2px"
    }
})

//COMPONENT=================================================================
function CategoryGrid(props) {
    const { visible, hideSidebar } = useContext(SidebarContext)
    const [showItems, setShowItems] = useState(false);
    const didMount = useDidMount();

    useEffect(() => {
        if(!didMount){
            setShowItems(false);
        }
    }, [visible])

    function renderItems() {
        const { url, id, nameField, amountField, items } = props;
        let key = 0;

        return items.map(
            (item) => {
                key++;
                return (
                    <Grid.Column
                        key={key}
                        className={itemClass}
                        as={Link}
                        to={ `/${url}/${item[id]}` }
                        onClick={hideSidebar}
                    >
                        <div>
                            {item[nameField]}
                            <Label color="black" tsize="mini" className={labelClass}>
                                {item[amountField]}
                            </Label>
                        </div>
                    </Grid.Column>
                )
            }
        )
    }

    function render() {
        const { name, items } = props;
        if(!items || !items.length){
            return null;
        }
        else{
            return (
                <Fragment>
                    <Grid.Row
                        className={headerRowClass}
                        columns={1}
                        onClick={() => setShowItems(!showItems)}
                    >
                        <Grid.Column>
                            <Header as="h3">
                                <Icon name="caret up" className={centerClass} />
                                {name}
                                <Icon name="caret down" flipped={showItems ? "vertically" : null} className={caretClass} />
                            </Header>
                        </Grid.Column>
                    </Grid.Row>
                    <Transition.Group animation="slide right" duration={300}>
                        {showItems &&
                            <Grid.Row columns={2} className={itemRowClass}>
                                {renderItems()}
                            </Grid.Row>
                        }
                    </Transition.Group>
                </Fragment>
            )
        }
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default CategoryGrid;