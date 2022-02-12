quack_grammar = """
    ?start: program
        
    ?program: statement*
    
    ?statement_block: "{" statement* "}"
    
    ?statement: l_op ";"
        | NAME "=" l_op
        | NAME ":" NAME "=" l_op ";"
        | "if" l_op                                         -> if_block
        | "while" l_op statement_block                      -> while_block
    
        
    // change name to expr?
    // l_op is a logical operator
    ?l_op: r_op
        | l_op "and" r_op                                   -> cond_and
        | l_op "or" r_op                                    -> cond_or
        // delete cond_not (it needs higher precedence )?
        | l_op "not" r_op                                   -> cond_not
        
    // r_op is a relational operator
    ?r_op: a_op
        | r_op "==" a_op                                    -> m_equals
        | r_op "<" a_op                                     -> m_less
        | r_op ">" a_op                                     -> m_more
        | r_op "<=" a_op                                    -> m_atmost
        | r_op ">=" a_op                                    -> m_atleast
    
    
    // a_op is an arithmetic operator
    ?a_op: a_product
        | a_op "+" a_product                                -> m_add
        | a_op "-" a_product                                -> m_sub
        | a_op "." NAME "(" args? ")"                       -> m_call
        
    ?args: l_op ("," l_op)*                                 -> m_args
        
    ?a_product: atom
        | a_product "*" atom                                -> m_mul
        | a_product "/" atom                                -> m_div
        
    ?atom: NUMBER                       -> lit_num
        | STRING                        -> lit_str
        // fix NAME -> var?
        | NAME                          -> var
        // change "-" l_op to "-" NUMBER
        | "-" l_op                      -> m_neg
        | "true"                        -> lit_true
        | "false"                       -> lit_false
        | "none"                        -> lit_none
        | "(" l_op ")" 
        // | "not" l_op                -> cond_not
        
    ?type: NAME
        

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE
    %import common.NEWLINE
    %import common.C_COMMENT
    %import common.CPP_COMMENT
    %import common.ESCAPED_STRING -> STRING
    // %import python.string -> STRING
    
    %ignore WS_INLINE
    %ignore NEWLINE
    %ignore C_COMMENT
    %ignore CPP_COMMENT
"""
