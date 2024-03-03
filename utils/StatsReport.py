


class Report:
    """
    Construct a statistical report
    ...
    Keyword Parameters
    ----------
    report_type: str
        Specified report type
        
    * For the Summary of Hypothesis Test::
        test_type: str
            The name and type of the test
        research_problem: str
        h0: str
            The null hypothesis
        h1: str
            The alternative (or research) hypothesis
        levelof_significance: float
            The specified level of significance
        crit_value: str
            The critical value
            Example:: 
                t >= 2.228 at the 0.05 level of significance, given df = 10
        act_value: str
            The actual value obtained after some calculations, takes the form
            of value = a_number
        decision: bool
            If True:: the null hypothesis is true, retain
            If False:: the null hypothesis is false, reject
        hypothesis: str
            The hypothesis that is either retained or rejected
        interpretation: str
    
    * For the one factor ANOVA table::
        experiment_name: str
        ss_between: float
        ss_within: float 
            -- For repeated measures --
                ss_subject: float
                ss_error: float
        df_between: int
        df_within: int 
            -- For repeated measures --
                df_subject: int
                df_error: int
        ms_between: float
        ms_within: float
        f_score: float
        
    * For the two factors ANOVA table::
        experiment_name: str
        ss_column: float
        ss_row: float
        ss_interaction: float
        ss_within: float
        df_column: int
        df_row: int
        df_interaction: int
        df_within: int
        ms_column: float
        ms_row: float
        ms_interation: float
        ms_within: float
        fscore_column: float
        fscore_row: float
        fscore_interaction: float
        
    * For differences between means:
        experiment_name: str
        tgroup_1: str
        tgroup_2: str
        tgroup_3: str
        tgroup_1_mean: float
        tgroup_2_mean: float
        tgroup_3_mean: float
    ----------
    """
    
    def __init__(self, report_type, **kwargs):
        self.report_type = report_type
        self.items = dict()
        for key, value in kwargs.items():
            self.items[key] = value
        
    def _repr_html_(self):
        if self.report_type == "summary":
            return f"""
                    <p>
                        <h2>HYPOTHESIS TEST SUMMARY</h2>
                        <h2>{self.items["test_type"]}</h2>
                        <ul>\
                            <li><b>Research Problem</b>
                                <p>{self.items["research_problem"]}.</p>
                            </li>
                            <li><b>Statistical Hypotheses</b>
                                <ul>
                                    <li>{self.items["h0"]}</li>
                                    <li>{self.items["h1"]}</li>
                                </ul>
                            </li>
                            <li><b>Decision Rule</b>
                                <p>
                                    Reject $H_0$ at the {self.items["levelof_significance"]} 
                                    level of significance if {self.items["crit_value"]}.
                                </p>
                            </li>
                            <li><b>Calculations</b>
                                <p>{self.items["act_value"]}.</p>
                            </li>
                            <li><b>Decision</b>
                                <p>
                                    {'Reject' if self.items["decision"] else 'Retain'} the {self.items["hypothesis"]} 
                                    at the {self.items["levelof_significance"]} level of significance
                                    because {self.items["act_value"]}.
                                </p>
                            </li>
                            <li><b>Interpretation</b>
                                <p>{self.items["interpretation"]}.</p>
                            </li>
                        </ul>
                    </p>
                    """
        
        if self.report_type == "one factor ANOVA":
            return f"""
                    <h3>ANOVA TABLE: {self.items["experiment_name"]}</h3>
                    <table>
                        <tr>
                            <b>
                            <th>SOURCE</th>
                            <th>SS</th>
                            <th>df</th>
                            <th>MS</th>
                            <th>F</th>
                            </b>
                        </tr>
                        <tr>
                            <td>Between</td>
                            <td>{self.items["ss_between"]}</td>
                            <td>{self.items["df_between"]}</td>
                            <td>{self.items["ms_between"]}</td>
                            <td>{self.items["f_score"]}</td>
                        </tr>
                        <tr>
                            <td>Within</td>
                            <td>{self.items["ss_within"]}</td>
                            <td>{self.items["df_within"]}</td>
                            <td>{self.items["ms_within"]}</td>
                        </tr>
                        <tr>
                            <td>Total</td>
                            <td>{self.items["ss_between"] + self.items["ss_within"]}</td>
                            <td>{self.items["df_between"] + self.items["df_within"]}</td>
                        </tr>
                    </table>
                    """
        
        if self.report_type == "repeated measures ANOVA":
            return f"""
                    <h3>ANOVA TABLE: {self.items["experiment_name"]}</h3>
                    <table>
                        <tr>
                            <b>
                            <th>SOURCE</th>
                            <th>SS</th>
                            <th>df</th>
                            <th>MS</th>
                            <th>F</th>
                            </b>
                        </tr>
                        <tr>
                            <td>Between</td>
                            <td>{self.items["ss_between"]}</td>
                            <td>{self.items["df_between"]}</td>
                            <td>{self.items["ms_between"]}</td>
                            <td>{self.items["f_score"]}</td>
                        </tr>
                        <tr>
                            <td>Within</td>
                            <td>{self.items["ss_within"]}</td>
                            <td>{self.items["df_within"]}</td>
                        </tr>
                        <tr>
                            <td>$\;\;$Subject</td>
                            <td>{self.items["ss_subject"]}</td>
                            <td>{self.items["df_subject"]}</td>
                        </tr>
                        <tr>
                            <td>$\;\;$Error</td>
                            <td>{self.items["ss_error"]}</td>
                            <td>{self.items["df_error"]}</td>
                            <td>{self.items["ms_error"]}</td>
                        </tr>
                        <tr>
                            <td>Total</td>
                            <td>{self.items["ss_between"] + self.items["ss_within"]}</td>
                            <td>{self.items["df_between"] + self.items["df_within"]}</td>
                        </tr>
                    </table>
                    """
         
        if self.report_type == "two factors ANOVA":
            ss_total = self.items["ss_column"] + self.items["ss_row"] + self.items["ss_interaction"] + self.items["ss_within"]
            df_total = self.items["df_column"] + self.items["df_row"] + self.items["df_interaction"] + self.items["df_within"]
            
            return f"""
                    <h3>ANOVA Table: {self.items["experiment_name"]}</h3>
                    <table>
                        <tr>
                            <b>
                            <th>SOURCE</th>
                            <th>SS</th>
                            <th>df</th>
                            <th>MS</th>
                            <th>F</th>
                            </b>
                        </tr>
                        <tr>
                            <td>Column</td>
                            <td>{self.items["ss_column"]}</td>
                            <td>{self.items["df_column"]}</td>
                            <td>{self.items["ms_column"]}</td>
                            <td>{self.items["fscore_column"]}</td>
                        </tr>
                        <tr>
                            <td>Row</td>
                            <td>{self.items["ss_row"]}</td>
                            <td>{self.items["df_row"]}</td>
                            <td>{self.items["ms_row"]}</td>
                            <td>{self.items["fscore_row"]}</td>
                        </tr>
                        <tr>
                            <td>Interaction</td>
                            <td>{self.items["ss_interaction"]}</td>
                            <td>{self.items["df_interaction"]}</td>
                            <td>{self.items["ms_interaction"]}</td>
                            <td>{self.items["fscore_interaction"]}</td>
                        </tr>
                        <tr>
                            <td>Within</td>
                            <td>{self.items["ss_within"]}</td>
                            <td>{self.items["df_within"]}</td>
                            <td>{self.items["ms_within"]}</td>
                        </tr>
                        <tr>
                            <td>Total</td>
                            <td>{ss_total}</td>
                            <td>{df_total}</td>
                        </tr>
                    </table>
                    """
            
        if self.report_type == "differences between means":
            return f"""
                    <h3>{self.items["experiment_name"]}</h3>
                    <table>
                        <tr>
                            <th></th>
                            <th>$X_{self.items["tgroup_1"]}$</th>
                            <th>$X_{self.items["tgroup_2"]}$</th>
                            <th>$X_{self.items["tgroup_3"]}$</th>
                        </tr>
                        <tr>
                            <td>$X_{self.items["tgroup_1"]}$</td>
                            <td></td>
                            <td>{abs(self.items["tgroup_2_mean"] - self.items["tgroup_1_mean"])}</td>
                            <td>{abs(self.items["tgroup_3_mean"] - self.items["tgroup_1_mean"])}</td>
                        </tr>
                        <tr>
                            <td>$X_{self.items["tgroup_2"]}$</td>
                            <td></td>
                            <td></td>
                            <td>{abs(self.items["tgroup_3_mean"] - self.items["tgroup_2_mean"])}</td>
                        </tr>
                        <tr>
                            <td>$X_{self.items["tgroup_3"]}$</td>
                            <td></td>
                            <td></td>
                            <td></td>
                        </tr>
                    </table>
                    """
        