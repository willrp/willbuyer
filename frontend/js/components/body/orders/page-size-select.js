//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { Dropdown } from "semantic-ui-react";

//COMPONENT=================================================================
function PageSizeSelect({ value, pageList, onChange }) {
    const pageOptions = pageList.map(
        (page) => {
            return {key: page, text: page + " orders", value: page}
        }
    )

    return(
        <Dropdown
            options={pageOptions}
            selection
            value={value}
            onChange={onChange}
        />
    )
}

//EXPORT COMPONENT==========================================================
export default PageSizeSelect;