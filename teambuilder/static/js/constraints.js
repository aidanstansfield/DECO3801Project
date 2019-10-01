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
        "should_bool" : shouldBool,
        "count_bxy" : [countMin, countMax],
        "with_bool" : withBool,
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
        return JSON.parse(JSON.stringify(params));
    }

    function toHTML() {
        var sentence = "<p>Each team ";
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
        "similar_bool" : shouldBool,
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
        var sentence = "<p>Each team ";
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