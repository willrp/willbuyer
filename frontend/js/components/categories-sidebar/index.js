//IMPORT EXTERNAL COMPONENTS================================================
import React, { useContext } from "react";
import { Grid } from "semantic-ui-react";

//IMPORT INTERNAL COMPONENTS================================================
import GenderGrid from "./gender-grid";
import CategoryGrid from "./category-grid";

//IMPORT CONTEXTS===========================================================
import { SidebarContext } from "contexts/sidebar-context";

// IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

// STYLE CLASSES DEFINITION==================================================
const gridClass = css({
    "&&&&": {
        margin: "0",
        backgroundColor: "lightskyblue"
    }
});

//COMPONENT=================================================================
function CategoriesSidebar() {
    const { sidesessions, sidebrands, sidekinds } = useContext(SidebarContext);

    return (
        <Grid
            className={gridClass}
            columns={2}
            celled
            textAlign="center"
        >
            <GenderGrid />
            <CategoryGrid name="Sessions" url="session" id="id" nameField="name" amountField="total" items={sidesessions} />
            <CategoryGrid name="Brands" url="brand" id="brand" nameField="brand" amountField="amount" items={sidebrands} />
            <CategoryGrid name="Kinds" url="kind" id="kind" nameField="kind" amountField="amount" items={sidekinds} />
        </Grid>
    )
}

//EXPORT COMPONENT==========================================================
export default CategoriesSidebar;