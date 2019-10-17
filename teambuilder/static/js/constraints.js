// This file contains definitions of constraints that are
// able to be used by the allocator. Note that the error
// checking of these constraints is limited to semantic
// correctness only. This is to allow for modularity.

// VALIDATION METHODS -----------------------------------------------
function isBoolean(value) {
    return typeof value === "boolean";
}

function isNumber(value) {
    return typeof value === "number" && isFinite(value);
}

function isString(value) {
    return typeof value === "string" || value instanceof String;
}

function isArray(value) {
    return value && typeof value === "object" && value.constructor === Array;
}

// CONSTRAINTS ------------------------------------------------------
var createObject = function(o) {
    function F() {}
    F.prototype = o
    return new F();
};

function IntegerCountConstraint(shouldBool, countMin, countMax,
    withBool, field, fieldMin, fieldMax) {
    // Each team <should/shouldn't> have between <min>
    // and <max> members <with/without> <field> between
    // <min> and <max>.

    var isError = false;
    var errMsg = "";

    if (!isNumber(countMin) || !isNumber(countMax) || countMin > countMax) {
        errMsg = "Invalid count constraint bounds";
        isError = true;
    } else if (!isBoolean(shouldBool) || !isBoolean(withBool)) {
        errMsg = "Invalid constraint boolean";
        isError = true;
    } else if (!isNumber(fieldMin) || !isNumber(fieldMax) || fieldMin > fieldMax) {
        errMsg = "Invalid count constraint values";
        isError = true;
    }

    var params = {
        "constr_type" : "IntegerCountConstraint",
        "name" : field + " constraint",
        "should_bool" : (shouldBool == 'true'),
        "count_bxy" : [countMin, countMax],
        "with_bool" : (withBool == 'true'),
        "field" : field,
        "value_bxy" : [fieldMin, fieldMax],
        "priority" : 1
    }

    function getField() {
        return params["field"];
    }

    function hasError() {
        return isError;
    }

    function getErrorMsg() {
        return errMsg;
    }

    function toJSON() {
        console.log(JSON.stringify(params));
        console.log(JSON.parse(JSON.stringify(params)));
        return JSON.parse(JSON.stringify(params));
    }

    function toHTML() {
        var sentence = "<p>Each group ";
        if (params["should_bool"]) {
            sentence += "<strong>SHOULD HAVE</strong> ";
        } else {
            sentence += "<strong>SHOULDN'T HAVE</strong> ";
        }
        sentence += "between ";
        sentence += "<strong>" + params["count_bxy"][0] + "</strong> ";
        sentence += "and "
        sentence += "<strong>" + params["count_bxy"][1] + "</strong> ";
        sentence += "members ";
        if (params["with_bool"]) {
            sentence += "<strong>WITH</strong> ";
        } else {
            sentence += "<strong>WITHOUT</strong> ";
        }
        sentence += "<strong>" + params["field"] + "</strong> ";
        sentence += "between ";
        sentence += "<strong>" + params["value_bxy"][0] + "</strong> ";
        sentence += "and "
        sentence += "<strong>" + params["value_bxy"][1] + "</strong>.";
        
        return sentence;
    }

    var result = createObject(IntegerCountConstraint.prototype)
    result.toJSON = toJSON;
    result.toHTML = toHTML;
    result.hasError = hasError;
    result.getErrorMsg = getErrorMsg;
    result.getField = getField;

    return result;
}

function IntegerAverageConstraint(shouldBool, field,
    fieldMin, fieldMax) {
    // Each team <should/shouldn't> have average <field> between
    // <min and <max>

    var isError = false;
    var errMsg = "";

    if (!isBoolean(shouldBool)) {
        errMsg = "Invalid constraint boolean";
        isError = true;
    } else if (!isNumber(fieldMin)) {
        errMsg = "Invalid minimum average";
        isError = true;
    } else if (!isNumber(fieldMax)) {
        errMsg = "Invalid maximum average";
        isError = true;
    } else if (fieldMin > fieldMax) {
        errMsg = "Min average cannot exceed max average"
        isError = true;
    }

    var params = {
        "constr_type" : "IntegerAverageConstraint",
        "name" : field + " constraint",
        "should_bool" : (shouldBool == 'true'),
        "field" : field,
        "priority" : 1,
        "average_bxy" : [fieldMin, fieldMax]
    }

    function getField() {
        return params["field"];
    }

    function hasError() {
        return isError;
    }

    function getErrorMsg() {
        return errMsg;
    }

    function toJSON() {
        return JSON.parse(JSON.stringify(params));
    }

    function toHTML() {
        var sentence = "<p>Each group ";
        console.log(typeof params["should_bool"]);
        if (params["should_bool"]) {
            sentence += "<strong>SHOULD HAVE</strong> ";
        } else {
            sentence += "<strong>SHOULDN'T HAVE</strong> ";
        }
        sentence += "average "
        sentence += "<strong>" + params["field"] + "</strong>";
        sentence += " between <strong>" + params["average_bxy"][0] + "</strong>";
        sentence += " and <strong>" + params["average_bxy"][1] + "</strong>";

        return sentence;
    }

    var result = createObject(IntegerAverageConstraint.prototype)
    result.toJSON = toJSON;
    result.toHTML = toHTML;
    result.hasError = hasError;
    result.getErrorMsg = getErrorMsg;
    result.getField = getField;

    return result;
}

function IntegerSimilarityConstraint(similarBool, field) {
    // Each team <should/shouldn't> have similar <field>

    var isError = false;
    var errMsg = "";

    if (!isBoolean(similarBool)) {
        errMsg = "Invalid constraint boolean";
        isError = true;
    }

    var params = {
        "constr_type" : "IntegerSimilarityConstraint",
        "name" : field + " constraint",
        "similar_bool" : (similarBool == 'true'),
        "field" : field,
        "priority" : 1
    }

    function getField() {
        return params["field"];
    }

    function hasError() {
        return isError;
    }

    function getErrorMsg() {
        return errMsg;
    }

    function toJSON() {
        return JSON.parse(JSON.stringify(params));
    }

    function toHTML() {
        var sentence = "<p>Each group ";
        if (params["similar_bool"]) {
            sentence += "<strong>SHOULD HAVE</strong> ";
        } else {
            sentence += "<strong>SHOULDN'T HAVE</strong> ";
        }
        sentence += "similar "
        sentence += "<strong>" + params["field"] + "</strong>";

        return sentence;
    }

    var result = createObject(IntegerSimilarityConstraint.prototype)
    result.toJSON = toJSON;
    result.toHTML = toHTML;
    result.hasError = hasError;
    result.getErrorMsg = getErrorMsg;
    result.getField = getField;

    return result;
}

function IntegerGlobalAverageConstraint(field) {
    // All teams should have similar <field>

    var isError = false;
    var errMsg = "";

    var params = {
        "constr_type" : "IntegerGlobalAverageConstraint",
        "name" : field + " constraint",
        "field" : field,
        "priority" : 1
    }

    function getField() {
        return params["field"];
    }

    function hasError() {
        return isError;
    }

    function getErrorMsg() {
        return errMsg;
    }

    function toJSON() {
        return JSON.parse(JSON.stringify(params));
    }

    function toHTML() {
        var sentence = "<p>All groups have similar " + params["field"];
        return sentence;
    }

    var result = createObject(IntegerSimilarityConstraint.prototype)
    result.toJSON = toJSON;
    result.toHTML = toHTML;
    result.hasError = hasError;
    result.getErrorMsg = getErrorMsg;
    result.getField = getField;

    return result;
}

function OptionCountConstraint(shouldBool, countMin, countMax,
    withBool, field, option) {
    // Each team <should/shouldn't> have between <min>
    // and <max> members <with/without> <field> equal to <option>

    var isError = false;
    var errMsg = "";

    if (!isNumber(countMin) || !isNumber(countMax) || countMin > countMax) {
        errMsg = "Invalid count constraint bounds";
        isError = true;
    } else if (!isBoolean(shouldBool)) {
        errMsg = "Invalid constraint boolean";
        isError = true;
    }

    var params = {
        "constr_type" : "OptionCountConstraint",
        "name" : field + " constraint",
        "should_bool" : (shouldBool == 'true'),
        "count_bxy" : [countMin, countMax],
        "with_bool" : (withBool == 'true'),
        "field" : field,
        "selection" : option,
        "candidates": [],
        "priority" : 1
    }

    function getField() {
        return params["field"];
    }

    function hasError() {
        return isError;
    }

    function getErrorMsg() {
        return errMsg;
    }

    function setCandidates(candidates) {
        if (isArray(candidates)) {
            params.candidates = [...candidates];
        }
    }

    function toJSON() {
        return JSON.parse(JSON.stringify(params));
    }

    function toHTML() {
        var sentence = "<p>Each group ";
        if (params["should_bool"]) {
            sentence += "<strong>SHOULD HAVE</strong> ";
        } else {
            sentence += "<strong>SHOULDN'T HAVE</strong> ";
        }
        sentence += "between ";
        sentence += "<strong>" + params["count_bxy"][0] + "</strong> ";
        sentence += "and "
        sentence += "<strong>" + params["count_bxy"][1] + "</strong> ";
        sentence += "members ";
        if (params["with_bool"]) {
            sentence += "<strong>WITH</strong> ";
        } else {
            sentence += "<strong>WITHOUT</strong> ";
        }
        sentence += "<strong>" + params["field"] + "</strong> ";
        sentence += "equal to ";
        sentence += "<strong>" + params["selection"] + "</strong> ";
        
        return sentence;
    }

    var result = createObject(OptionCountConstraint.prototype)
    result.toJSON = toJSON;
    result.toHTML = toHTML;
    result.hasError = hasError;
    result.getErrorMsg = getErrorMsg;
    result.setCandidates = setCandidates;
    result.getField = getField;

    return result;
}

function OptionSimilarityConstraint(shouldBool, field) {
    // Each team <should/shouldn't> have similar <field>

    var isError = false;
    var errMsg = "";

    if (!isBoolean(shouldBool)) {
        errMsg = "Invalid constraint boolean";
        isError = true;
    }

    var params = {
        "constr_type" : "OptionSimilarityConstraint",
        "name" : field + " constraint",
        "similar_bool" : (shouldBool == 'true'),
        "field" : field,
        "candidates" : [],
        "priority" : 1
    }

    function getField() {
        return params["field"];
    }

    function hasError() {
        return isError;
    }

    function getErrorMsg() {
        return errMsg;
    }

    function toJSON() {
        return JSON.parse(JSON.stringify(params));
    }

    function setCandidates(candidates) {
        if (isArray(candidates)) {
            params.candidates = [...candidates];
        }
    }

    function toHTML() {
        var sentence = "<p>Each group ";
        if (params["similar_bool"]) {
            sentence += "<strong>SHOULD HAVE</strong> ";
        } else {
            sentence += "<strong>SHOULDN'T HAVE</strong> ";
        }
        sentence += "similar "
        sentence += "<strong>" + params["field"] + "</strong>";

        return sentence;
    }

    var result = createObject(OptionSimilarityConstraint.prototype)
    result.toJSON = toJSON;
    result.toHTML = toHTML;
    result.setCandidates = setCandidates;
    result.hasError = hasError;
    result.getErrorMsg = getErrorMsg;
    result.getField = getField;

    return result;
}

function SubsetCountConstraint(shouldBool, countMin, countMax,
    withBool, field, option) {
    // Each team <should/shouldn't> have between <min>
    // and <max> members <with/without> <field> containing <option>

    var isError = false;
    var errMsg = "";

    if (!isNumber(countMin) || !isNumber(countMax) || countMin > countMax) {
        errMsg = "Invalid count constraint bounds";
        isError = true;
    } else if (!isBoolean(shouldBool)) {
        errMsg = "Invalid constraint boolean";
        isError = true;
    }

    var params = {
        "constr_type" : "SubsetCountConstraint",
        "name" : field + " constraint",
        "should_bool" : (shouldBool == 'true'),
        "count_bxy" : [countMin, countMax],
        "with_bool" : (withBool == 'true'),
        "field" : field,
        "selection" : option,
        "candidates": [],
        "priority" : 1
    }

    function getField() {
        return params["field"];
    }

    function hasError() {
        return isError;
    }

    function getErrorMsg() {
        return errMsg;
    }

    function setCandidates(candidates) {
        if (isArray(candidates)) {
            params.candidates = [...candidates];
        }
    }

    function toJSON() {
        return JSON.parse(JSON.stringify(params));
    }

    function toHTML() {
        var sentence = "<p>Each group ";
        if (params["should_bool"]) {
            sentence += "<strong>SHOULD HAVE</strong> ";
        } else {
            sentence += "<strong>SHOULDN'T HAVE</strong> ";
        }
        sentence += "between ";
        sentence += "<strong>" + params["count_bxy"][0] + "</strong> ";
        sentence += "and "
        sentence += "<strong>" + params["count_bxy"][1] + "</strong> ";
        sentence += "members ";
        if (params["with_bool"]) {
            sentence += "<strong>WITH</strong> ";
        } else {
            sentence += "<strong>WITHOUT</strong> ";
        }
        sentence += "<strong>" + params["field"] + "</strong> ";
        sentence += "containing ";
        sentence += "<strong>" + params["selection"] + "</strong> ";
        
        return sentence;
    }

    var result = createObject(SubsetCountConstraint.prototype)
    result.toJSON = toJSON;
    result.toHTML = toHTML;
    result.hasError = hasError;
    result.getErrorMsg = getErrorMsg;
    result.setCandidates = setCandidates;
    result.getField = getField;

    return result;
}

function SubsetSimilarityConstraint(shouldBool, field) {
    // Each team <should/shouldn't> have similar <field>

    var isError = false;
    var errMsg = "";

    if (!isBoolean(shouldBool)) {
        errMsg = "Invalid constraint boolean";
        isError = true;
    }

    var params = {
        "constr_type" : "SubsetSimilarityConstraint",
        "name" : field + " constraint",
        "similar_bool" : (shouldBool == 'true'),
        "field" : field,
        "candidates" : [],
        "priority" : 1
    }

    function getField() {
        return params["field"];
    }

    function hasError() {
        return isError;
    }

    function getErrorMsg() {
        return errMsg;
    }

    function toJSON() {
        return JSON.parse(JSON.stringify(params));
    }

    function setCandidates(candidates) {
        if (isArray(candidates)) {
            params.candidates = [...candidates];
        }
    }

    function toHTML() {
        var sentence = "<p>Each group ";
        if (params["similar_bool"]) {
            sentence += "<strong>SHOULD HAVE</strong> ";
        } else {
            sentence += "<strong>SHOULDN'T HAVE</strong> ";
        }
        sentence += "similar "
        sentence += "<strong>" + params["field"] + "</strong>";

        return sentence;
    }

    var result = createObject(SubsetSimilarityConstraint.prototype)
    result.toJSON = toJSON;
    result.toHTML = toHTML;
    result.setCandidates = setCandidates;
    result.hasError = hasError;
    result.getErrorMsg = getErrorMsg;
    result.getField = getField;

    return result;
}

function BooleanCountConstraint(shouldBool, countMin, countMax,
    withBool, field) {
    // Each team <should/shouldn't> have between <min>
    // and <max> members <with/without> <field>

    var isError = false;
    var errMsg = "";

    if (!isNumber(countMin) || !isNumber(countMax) || countMin > countMax) {
        errMsg = "Invalid count constraint bounds";
        isError = true;
    } else if (!isBoolean(shouldBool)) {
        errMsg = "Invalid constraint boolean";
        isError = true;
    }

    var params = {
        "constr_type" : "BooleanCountConstraint",
        "name" : field + " constraint",
        "should_bool" : (shouldBool == 'true'),
        "count_bxy" : [countMin, countMax],
        "with_bool" : (withBool == 'true'),
        "field" : field,
        "priority" : 1
    }

    function getField() {
        return params["field"];
    }

    function hasError() {
        return isError;
    }

    function getErrorMsg() {
        return errMsg;
    }

    function setCandidates(candidates) {
        if (isArray(candidates)) {
            params.candidates = [...candidates];
        }
    }

    function toJSON() {
        return JSON.parse(JSON.stringify(params));
    }

    function toHTML() {
        var sentence = "<p>Each group ";
        if (params["should_bool"]) {
            sentence += "<strong>SHOULD HAVE</strong> ";
        } else {
            sentence += "<strong>SHOULDN'T HAVE</strong> ";
        }
        sentence += "between ";
        sentence += "<strong>" + params["count_bxy"][0] + "</strong> ";
        sentence += "and "
        sentence += "<strong>" + params["count_bxy"][1] + "</strong> ";
        sentence += "members ";
        if (params["with_bool"]) {
            sentence += "<strong>WITH</strong> ";
        } else {
            sentence += "<strong>WITHOUT</strong> ";
        }
        sentence += "<strong>" + params["field"] + "</strong> ";
        
        return sentence;
    }

    var result = createObject(OptionCountConstraint.prototype)
    result.toJSON = toJSON;
    result.toHTML = toHTML;
    result.hasError = hasError;
    result.getErrorMsg = getErrorMsg;
    result.setCandidates = setCandidates;
    result.getField = getField;

    return result;
}