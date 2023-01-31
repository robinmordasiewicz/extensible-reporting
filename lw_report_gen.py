import sys
import os
import json
import logzero
from pathlib import Path
import datetime
from logzero import logger
from modules.process_args import get_validated_arguments
from modules.utils import LaceworkTime
from modules.utils import get_available_reports
from modules.utils import alert_new_release
from modules.reportgen import ReportGen # do not remove, needed by pyinstaller

def main():

    # Get the base directory where this script is running from
    # Required for Pyinstaller as it temporarily extracts all files to a temp folder before running
    if getattr(sys, 'frozen', False):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(os.path.abspath(__file__))

    # Set up default logging level
    logzero.loglevel(logzero.WARNING)
    # Setup up log file, always write verbose logs
    logzero.logfile('lw_report_gen.log', loglevel=logzero.DEBUG)

    # check github for updates
    alert_new_release()

    # Dynamically import report classes from "modules/reports" subdirectory
    available_reports: list = get_available_reports(basedir)
    if len(available_reports) == 0:
        logger.debug('No available reports to run. You should not get this error since there is a default report so.... beats me.')
        sys.exit()
    # Get command line args and process them
    args = get_validated_arguments()

    # Print out available reports to run if the "--list-reports" flag was used
    if args.list_reports:
        print(f'\nAvailable Reports (use the "ID" with the "--report" flag to specify one):\n')
        for available_report in available_reports:
            print(f"{'(*Default) ' if available_report['report_short_name'] == 'CSA' else ''}ID:{available_report['report_short_name']}", end=" ")
            print(f"Name:{available_report['report_name']}", end=" ")
            print(f"Description: {available_report['report_description']}")
        print('')
        sys.exit()

    # Set loglevel to standard out based on verbosity arg
    if args.v:
        logzero.loglevel(logzero.INFO)
    elif args.vv:
        logzero.loglevel(logzero.DEBUG)
    # Convert query time args to a date format the Lacework API understands
    vulns_start_time = LaceworkTime(args.vulns_start_time)
    vulns_end_time = LaceworkTime(args.vulns_end_time)
    alerts_start_time = LaceworkTime(args.alerts_start_time)
    alerts_end_time = LaceworkTime(args.alerts_end_time)
    # Check to see if creds were provided
    api_key_file = None
    lacework_toml_exists = Path(str(Path.home()) + '/.lacework.toml').exists()
    env_var_creds_exist = bool(os.environ.get('LW_ACCOUNT')) and\
        bool(os.environ.get('LW_API_KEY')) and\
        bool(os.environ.get('LW_API_SECRET'))
    # If there's an API keyfile specified, try to use it, else exit
    if args.api_key_file:
        try:
            with open(args.api_key_file, 'r') as file:
                api_key_file = json.load(file)
        except Exception as e:
            logger.error(f"Failed to read keyfile: {str(e)}")
            sys.exit()
    elif not lacework_toml_exists and not env_var_creds_exist:
        logger.error("You have failed to provide Lacework API credentials")
        logger.error("Please read the github page for instructions.")
        logger.error("https://github.com/lacework/extensible-reporting")
        sys.exit()
    # search the list of available reports for the one specified on the command line. CSA is the default arg
    report_to_run = [report['report_class'] for report in available_reports if report['report_short_name'] == args.report][0]
    # Execute the selected report
    try:
        report_generator = report_to_run(basedir, use_cache=args.cache_data, api_key_file=api_key_file)
        report = report_generator.generate(args.customer,
                              args.author,
                              vulns_start_time=vulns_start_time,
                              vulns_end_time=vulns_end_time,
                              alerts_start_time=alerts_start_time,
                              alerts_end_time=alerts_end_time)
    except Exception as e:
        logger.error(f"Report Generation failed for report {args.report}, did you specify one that exists? Check what's available with the '--list-reports' flag.")
        logger.error("Exiting....")
        logger.error(str(e))
        sys.exit()

    # Generate a filename if one was not specified
    if not args.report_path:
        report_file_name = f'{args.customer}_{args.report}_{datetime.datetime.now().strftime("%Y%m%d")}.html'
    else:
        report_file_name = args.report_path
    # Write out the report file
    logger.info(f'Writing report to {args.report_path}')
    try:
        with open(str(report_file_name), 'w') as file:
            file.write(report)
    except Exception as e:
        logger.error(f'Failed writing report file {args.report_path}: {str(e)}')
        sys.exit()


if __name__ == "__main__":
    main()
