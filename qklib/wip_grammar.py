quack_grammar = """
    ?start: program
        
    ?program: class* statement*
    ?class: class_sig class_body -> _class
    ?class_sig: "class" IDENT "(" formal_args ")" [ "extends" IDENT ] -> class_sig
    ?formal_args: [IDENT ":" IDENT ("," IDENT ":" IDENT)* ] -> formal_args
    ?class_body: "{" statement* method* "}" -> class_body
    
    ?method: "def" IDENT "(" formal_args ")" [":" IDENT] statement_block -> method 
    
    ?statement_block: "{" statement* "}" -> statement_block
    
    ?statement: "if" l_op statement_block ("elif" l_op statement_block)* ["else" statement_block] -> if_block
        | "while" l_op statement_block -> while_block
        | assignment
        | "return" [l_op] ";" -> return_expr
        | "typecase" l_op "{" type_alt* "}" -> typecase
        | l_op ";" 
        
    ?type_alt: IDENT ":" IDENT statement_block -> type_alt 
    
    ?assignment: IDENT [":" IDENT] "=" l_op ";" -> assignment
        | expr "=" l_op ";" -> store_field
        
    
    
    // l_op is a logical operator
    ?l_op: r_op
        | l_op "and" r_op                                   -> cond_and
        | l_op "or" r_op                                    -> cond_or
        
    // r_op is a relational operator
    ?r_op: a_op
        | r_op "==" a_op                                    -> m_equal
        | r_op "!=" a_op                                    -> m_notequal
        | r_op "<" a_op                                     -> m_less
        | r_op ">" a_op                                     -> m_more
        | r_op "<=" a_op                                    -> m_atmost
        | r_op ">=" a_op                                    -> m_atleast
    
    
    // a_op is an arithmetic operator
    ?a_op: a_product
        | a_op "+" a_product                                -> m_add
        | a_op "-" a_product                                -> m_sub
        
    // actual_args
    ?args: l_op ("," l_op)*                                 -> m_args
        
    ?a_product: expr
        | a_product "*" expr                                -> m_mul
        | a_product "/" expr                                -> m_div
        
    //TODO: switch order of expr and unary_expr
    ?expr: unary_expr
        | expr "." IDENT "(" args? ")" -> m_call
        | expr "." IDENT -> load_field
        | IDENT "(" args? ")" -> c_call
        
        
    ?unary_expr: atom
        // change "-" l_op to "-" NUMBER
        | "-" l_op -> m_neg
        | "not" l_op                    -> cond_not
        
    ?atom: INT                       -> lit_num
        | STRING                        -> lit_str
        | IDENT                          -> var
        | "none"                     -> lit_nothing
        | "true"                        -> lit_true
        | "false"                       -> lit_false
        | "(" l_op ")" 
        
        
        
    STRING: ESCAPED_STRING | LONG_STRING

    %import common.CNAME -> IDENT
    %import common.INT
    %import common.ESCAPED_STRING
    %import python.LONG_STRING
    
    %import common.WS_INLINE
    %import common.NEWLINE
    %import common.C_COMMENT
    %import common.CPP_COMMENT
    
    %ignore WS_INLINE
    %ignore NEWLINE
    %ignore C_COMMENT
    %ignore CPP_COMMENT
"""
