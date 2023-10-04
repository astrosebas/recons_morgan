import os
import datetime
import pathlib
import json
import base64
import math
import astropy.units as u
from astropy.coordinates import Angle
from enum import IntEnum


class LogLevel(IntEnum):
    FATAL = 0    # blocks execution
    WARN = 1     # can become an issue
    INFO = 2     # standard log for information
    DEBUG = 3    # detailed debugging
    REPORT = 4   # log for reporting

class StatusId(IntEnum):
    """Enum for status."""
    # TODO: define behaviour for various type of errors
    FATAL = -1
    FAIL = 0
    SUCCESS = 1
    NO_DISK_SPACE = 2        # fatal
    LOW_DISK_SPACE = 3       # warning
    FILE_EXISTS = 4          # output file already exists, do not
    # overwrite (abort or start in another
    # directory?)
    UNEXPECTED_FORMAT = 5    # file content is not waht we expect, abort or warn ?
    STARTED = 6

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log(self, status, log_text, log_level):
    """Logs, execution status and optional text for tracing and status"""

    timestamp = datetime.datetime.utcnow()
    human_log = "[{}] {}:{}:{} - {}\n".format(
        timestamp.strftime("%d/%m/%Y - %H:%M:%S"),
        self.current_module, log_level.name, status.name, log_text)
    print(human_log, end='')
    self.log_human[self.current_module].write(human_log)
    parsable_log = ("{{{{{}}},"
                    + "{{{}}},"
                    + "{{{}}},"
                    + "{{{}}},"
                    + "{{{}}}}}\n").format(
        timestamp.isoformat(), self.current_module,
                        log_level, status, base64.b64encode(
                            log_text.encode("utf-8")).decode('utf-8'))
    self.log_parsable[self.current_module].write(parsable_log)

class StatusLogger:
    """Reporting to log file, as human readable and parsable."""

    def __init__(self):
        self.log_dir = {}
        self.log_filename_human = {}
        self.log_filename_parsable = {}
        self.log_human = {}
        self.log_parsable = {}

        self.modules_status = {}
        self.log_level = LogLevel.WARN
        self.debug = self.debug_pass

    def init_global(self, base_dir):
        self.init_module('global', base_dir, mode='a')

    def init_module(self, module, log_dir, mode="w"):
        """Init log file in output directory, makes a new file.
        Each run restarts the log file, avoids clashes of data.
        If data does not need to be regenerated, it shouldn't. But
        log to report should always store data"""

        self.current_module = module
        self.log_dir[self.current_module] = log_dir
        # check that log_dir exists
        working_dir = pathlib.Path(log_dir)
        if not working_dir.exists():
            working_dir.mkdir(exist_ok=False)

        self.log_filename_human[self.current_module] = str(
            log_dir / (module + "_pipeline.log"))
        self.log_filename_parsable[self.current_module] = str(
            log_dir / (module + "_pipeline.parsable"))
        self.log_human[self.current_module] = open(
            self.log_filename_human[self.current_module],
            mode,
            encoding="utf-8")
        self.log_parsable[self.current_module] = open(
            self.log_filename_parsable[self.current_module],
            mode,
            encoding="utf-8")

    def log(self, status, log_text, log_level):
        """Logs, execution status and optional text for tracing and status"""
        # TODO: should we log some data ? could store exception data
        # TODO: Sould we open/close file each time?
        # TODO: use loglevel

        # if self.log_level == LogLevel.DEBUG and self.log_debug == False:
        #     return

        timestamp = datetime.datetime.utcnow()
        human_log = "[{}] {}:{}:{} - {}\n".format(
            timestamp.strftime("%d/%m/%Y - %H:%M:%S"),
            self.current_module, log_level.name, status.name, log_text)
        print(human_log, end='')
        self.log_human[self.current_module].write(human_log)
        parsable_log = ("{{{{{}}},"
                        + "{{{}}},"
                        + "{{{}}},"
                        + "{{{}}},"
                        + "{{{}}}}}\n").format(
            timestamp.isoformat(), self.current_module,
                            log_level, status, base64.b64encode(
                                log_text.encode("utf-8")).decode('utf-8'))
        self.log_parsable[self.current_module].write(parsable_log)

    def set_log_level(self, loglevel):
        if loglevel == 'debug':
            self.log_level = LogLevel.DEBUG
            self.debug = self.debug_print
        else:
            self.log_level = LogLevel.WARN
            self.debug = self.debug_pass

    def info(self, text):
        """Shorthand for info log"""
        self.log(StatusId.SUCCESS, text, LogLevel.INFO)

    def debug_print(self, text):
        """Shorthand for debug log"""
        self.log(StatusId.SUCCESS, text, LogLevel.DEBUG)

    def debug_pass(self, text):
        """Shorthand for debug log"""
        pass

    def warn(self, text):
        """Shorthand for warning log"""
        self.log(StatusId.FAIL, text, LogLevel.WARN)

    def fatal(self, text):
        """Shorthand for fatal log that also throws an exception"""
        self.log(StatusId.FAIL, text, LogLevel.FATAL)
        raise PipelineFatalException()

    def report(self, report_key, report_data):
        """Store data for inclusion in report"""
        # Data about pipeline execution can be stored this way,
        # analysis data might be tricky to store in here.

        data = {report_key: report_data}
        serialized_data = json.dumps(data)
        log.log(StatusId.SUCCESS,
                serialized_data, LogLevel.REPORT)

    def get_report_dict_for_module(self, module):
        '''Gets a dictionary of report values stored for the report.'''
        data_dict = {}

        # need to flush the file to disk before running this
        # TODO: check policy here, but we might want to keep the file
        # open to write errors in logging/reporting to it
        # or use a open/write log/close cycle on each log

        self.log_parsable[module].flush()

        log_parsable = open(
            self.log_filename_parsable[module], "r", encoding="utf-8")

        regex = re.compile("\{\{(?P<timestamp>.*)\},"
                           + "\{(?P<module>.*)\},"
                           + "\{(?P<loglevel>.*)\},"
                           + "\{(?P<status>.*)\},"
                           + "\{(?P<data>.*)\}\}")
        for l in log_parsable:
            m = regex.match(l)
            if m is not None:
                loglevel = LogLevel(int(m.group('loglevel')))
                if (m.group('module') == module and loglevel == LogLevel.REPORT):
                    d = base64.b64decode(
                        m.group('data').encode('utf-8')).decode("utf-8")
                    # print(type(d), d)
                    p = json.loads(d)

                    data_dict.update(p)
            else:
                print("Weird log line: ", l)

        return data_dict

    def build_report_file(self, template_file,
                          output_file, report_vars_dictionary, filters={}):
        '''Make a chunk of report from the templating engine'''
        # prepare tex engine and templates
        latex_jinja_env = jinja2.Environment(
            block_start_string='\BLOCK{',
            block_end_string='}',
            variable_start_string='\VAR{',
            variable_end_string='}',
            comment_start_string='\#{',
            comment_end_string='}',
            line_statement_prefix='%%',
            line_comment_prefix='%#',
            trim_blocks=True,
            autoescape=False,
            loader=jinja2.FileSystemLoader(os.path.abspath('./templates'))
        )

        for n, f in filters.items():
            latex_jinja_env.filters[n] = f
        # adding the zip command as filter to the engine
        latex_jinja_env.filters['zip'] = zip
        template = latex_jinja_env.get_template(template_file)

        # create report
        report_string = template.render(report_vars_dictionary)

        f = output_file.open("w",encoding="utf8")
        f.write(report_string)

    def build_section_report(self,
                             working_dir,
                             report_dir,
                             report_filename,
                             sections=[],
                             dualpass=False):
        """Make a report including section files from the input"""

        # TODO: check availability of subreport files
        # report on availability

        report_vars = {'sections': sections}
        if not working_dir.exists():
            print("No data dir")
            # TODO: log fail?

        template_filename = "global_report.tex"

        # read from template, output to current working dir
        log.build_report_file(
            template_filename,
            working_dir / report_dir / report_filename,
            report_vars)

        # generate PDF
        log.generate_pdf_report_from_tex(working_dir,
                                         report_dir,
                                         report_dir / report_filename)

        if dualpass:
            log.generate_pdf_report_from_tex(working_dir,
                                             report_dir,
                                             report_dir / report_filename)

    def set_current_module(self, module):
        self.current_module = module

    def set_module_status(self, module, status):
        self.set_current_module(module)
        print("register {} {}".format(module, status.name))
        if status == StatusId.STARTED:
            self.report('started', True)
        elif status == StatusId.SUCCESS:
            # TODO: should this unset the module name?
            self.report('completed_status', True)
        elif status == StatusId.FAIL:
            self.report('completed_status', False)

    def gen_module_run_summary(self, module):

        data_dict_report = {}
        data_dict_warn = {}
        data_dict_fatal = {}

        self.log_parsable[module].flush()

        log_parsable = open(
            self.log_filename_parsable[module], "r", encoding="utf-8")

        regex = re.compile("\{\{(?P<timestamp>.*)\},"
                           + "\{(?P<module>.*)\},"
                           + "\{(?P<loglevel>.*)\},"
                           + "\{(?P<status>.*)\},"
                           + "\{(?P<data>.*)\}\}")

        warn_list = []
        fatal_list = []

        for l in log_parsable:
            m = regex.match(l)

            if m is not None:
                loglevel = LogLevel(int(m.group('loglevel')))
                if m.group('module') == module:
                    d = base64.b64decode(
                        m.group('data').encode('utf-8')).decode("utf-8")
                    timestamp = m.group('timestamp')
                    if loglevel == LogLevel.REPORT:
                        p = json.loads(d)
                        data_dict_report.update(p)
                    elif loglevel == LogLevel.WARN:
                        p = d
                        warn_list.append((timestamp, p))
                    elif loglevel == LogLevel.FATAL:
                        p = d
                        fatal_list.append((timestamp, p))
            else:
                print("Weird log line: ", l)

        started = False
        completed_status = False
        if 'started' in data_dict_report:
            started = data_dict_report['started']

        if 'completed_status' in data_dict_report:
            completed_status = data_dict_report['completed_status']

        num_warn = len(warn_list)
        num_fatal = len(fatal_list)

        data_dict = {
            'summary_started': started,
            'summary_status': completed_status,
            'summary_num_warn': num_warn,
            'summary_num_fatal': num_fatal,
        }

        log_list = {"warnings": warn_list, "fatal": fatal_list}

        return data_dict, log_list

    def generate_pdf_report_from_tex(self, working_dir, output_dir, source_tex):
        """make a pdf from tex file.
        working_dir: base dir where pdf_latex is run, path are looked up from there
        output_dir: where to output the data
        source_tex: path for input tex file
        """
#        log.info("Starting pdflatex on {} "
#                 "in directory {} "
#                 "output to {}".format(str(source_tex), working_dir,
#                                       output_dir))
        returnstatus = subprocess.run(['lualatex',
                                       "-interaction",
                                       "nonstopmode",
                                       '-output-directory',
                                       str(output_dir),
                                       str(source_tex)],
                                      cwd=str(working_dir),
                                      # stdout=subprocess.DEVNULL)  # option to suppress output
                                      )
#        if returnstatus.returncode == 0:
#            log.info("PDF generation process returned with 0 return code")
#        else:
#            log.warn("PDF generation process returned "
#                     "with non zero return code: {}".format(returnstatus.returncode))


log = StatusLogger()


def degree_to_dms(deg):
    if deg is None:
        return ""
    d = Angle(deg, u.deg)
    return d.to_string(format='latex', unit=u.deg)


def degree_to_hms(deg):
    if deg is None:
        return ""

    d = Angle(deg, u.deg)
    return d.to_string(format='latex', unit=u.hour)


def degree_to_mas(deg):
    if deg is None:
        return ""

    d = deg * 1000.0 * 3600.0
    return "{:.1f}".format(d)


