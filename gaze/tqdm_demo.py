from tqdm import tqdm


def main():
    # Wrap tqdm() around any iterable
    for i in tqdm(range(10000)):
        pass


if __name__ == '__main__':
    main()
